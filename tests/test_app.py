import httpx
import uvicorn
import asyncio

import json
from typing import List
import random
import populate_db as populate_db 

from db.session_provider import get_db_session
from models.models import UserInDb
from schemas.auth_data import AuthData
from schemas.users_data import UserActivationData, UserInfoData, UserCreationData
from schemas.loans_data import LoanRequestData, LoanResponseData, LoanInfoData

from main import app

from populate_db import get_old_password, get_new_password, original_users_dict

#______________________________________________________________________________
#
# region 1 : auth login
#______________________________________________________________________________
async def test_login():
    """Test pour obtenir un token d'accès valide"""

    user_data = original_users_dict["admin"]
    response = await get_login_response(user_data)

    if response.status_code == 200 :
        print ("test_login : OK")
        #print (response.json().get("access_token"))
    else : 
        print ("test_login : errors / ko")
        

async def get_login_response(user_data : UserCreationData) :
    
    auth_data = AuthData(
        email=user_data.email, 
        password=user_data.password)
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/auth/login",
             data = auth_data.model_dump_json())

        return response
    
def get_token(loginresponse):
    access_token = loginresponse.json().get("access_token")
    return access_token

def get_headers(jwt_token) :
    str_token = str(jwt_token)
    headers = {
        'Authorization': f'Bearer {str_token}',  # Ajout du token dans l'en-tête Authorization
    }
    return headers

#______________________________________________________________________________
#
# region 2 : auth activation
#______________________________________________________________________________
async def test_activation():

    # select unactivated user 
    db_session = next(get_db_session())
    inactive_user = db_session.query(UserInDb).filter(UserInDb.is_active==False).first()
    if not inactive_user :
        print ("test_activation : errors / ko ... (no inactive user in db)")
        return

    inactive_user_creation_data = UserCreationData(
        email = inactive_user.email,
        username= inactive_user.username,
        role = inactive_user.role,
        password = get_old_password(inactive_user.username)
    )
    
    inactive_user_login_response = await get_login_response(inactive_user_creation_data)
    jwt_token = get_token(inactive_user_login_response)
    headers = get_headers(jwt_token)

    # Données d'activation
    activation_data = UserActivationData(
        new_password = get_new_password(inactive_user.username))
    
    # Appel à la route d'activation
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/auth/activation", 
            data=activation_data.model_dump_json(), 
            headers= headers)

    # Vérifications
    if response.status_code == 200 :
        print ("test_activation : OK")
    else : 
        print ("test_activation : errors / ko")
    #assert response.json()["msg"] == "Account activated and password updated successfully."


#______________________________________________________________________________
#
# region auth logout
#______________________________________________________________________________
async def test_logout():
    
    user_data = original_users_dict["active_user"]

    admin_login_response = await get_login_response(user_data)
    jwt_token = get_token(admin_login_response)
    headers = get_headers(jwt_token)

    # Appel à la route de déconnexion
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/auth/logout", 
        headers=headers)

    # Vérifications

    if response.status_code == 200 :
        print ("test_logout: OK")
        #print(response.json())
    else : 
        print ("test_logout : errors / ko")

    # assert response.json()["msg"] == "Logged out successfully. Token is invalidated."

#______________________________________________________________________________
#
# region 3 : loans request
#______________________________________________________________________________
async def test_loans_request():

    user_data = original_users_dict["active_user"]

    user_login_response = await get_login_response(user_data)
    jwt_token = get_token(user_login_response)
    headers = get_headers(jwt_token)

    # Données de la demande de prêt
    loan_request_data = LoanRequestData(
        state = "OH",
        bank = "CAPITAL ONE NATL ASSOC",
        naics = 54, 
        term = 6,
        no_emp = 13,
        new_exist = 1,
        create_job = 0,
        retained_job = 3,
        urban_rural = 2,
        rev_line_cr= 0,
        low_doc = 0,
        gr_appv = 50000,
        recession = 1,
        has_franchise = 1
    )

    # Appel à la route de soumission de la demande de prêt
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/loans/request", 
            data=loan_request_data.model_dump_json(), 
            headers=headers)

    # Vérifications
    if response.status_code == 200 :
        print ("test_loans_request: OK")
    else : 
        print ("test_loans_request : errors / ko")

    # assert response.json() == {"msg": "Loan request submitted successfully."}


#______________________________________________________________________________
#
# region 4 : loans history
#______________________________________________________________________________
async def test_loans_history():

    user_data = original_users_dict["active_user"]

    user_login_response = await get_login_response(user_data)
    jwt_token = get_token(user_login_response)
    headers = get_headers(jwt_token)

    # Appel à la route d'historique des demandes de prêt
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://127.0.0.1:8000/loans/history", 
            headers=headers)

    # Vérifications
    if response.status_code == 200 :
        print ("test_loans_history : OK")
    else : 
        print ("test_loans_history : errors / ko")

    # loan_history = response.json()["loan_history"]
    # assert len(loan_history) == 2  # Vérifie que deux demandes de prêt sont retournées
    # assert loan_history[0]["amount"] == 10000  # Vérifie que la première demande a bien le montant attendu
    # assert loan_history[1]["amount"] == 5000  # Vérifie que la deuxième demande a bien le montant attendu

#______________________________________________________________________________
#
# region 5 : admin users
#______________________________________________________________________________
async def test_get_users():

    admin_data = original_users_dict["admin"]

    admin_login_response = await get_login_response(admin_data)
    jwt_token = get_token(admin_login_response)
    headers = get_headers(jwt_token)

    # Envoie une requête GET pour récupérer la liste des utilisateurs
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://127.0.0.1:8000/admin/users", 
            headers=headers )

    # Vérifie la réponse et les résultats attendus
    if response.status_code == 200 :
        print ("test_get_users : OK")
    else : 
        print ("test_get_users : errors / ko")
    
    # users = []
    # try : 
    #     json_data = response.json()
    #     users : List[UserInfoData] = [UserInfoData.model_validate(user_data) for user_data in json_data]
    # except:
    #     pass
    
    # for user in users : 
    #     print(user)

#______________________________________________________________________________
#
# region 6 : create_user
#______________________________________________________________________________
async def test_create_user():
    
    admin_data = original_users_dict["admin"]

    admin_login_response = await get_login_response(admin_data)
    jwt_token = get_token(admin_login_response)
    headers = get_headers(jwt_token)
    
    n = str(random.randint(3, 99))

    proto_email = "user" +str(n) + ".fakemail@fakeprovider.com"
    proto_username = "User"+ str(n)

    # Données utilisateur à envoyer
    user_data = UserCreationData(
        email = proto_email,
        username = proto_username, 
        role = "user",
        password= get_old_password(proto_username))
    

    # Simuler l'appel à la route de création d'utilisateur
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/admin/users", 
            data = user_data.model_dump_json(),
            headers = headers)

    # Vérifications
    if response.status_code == 200 :
        print ("test_create_user : OK")
        #print(response.json())
    else : 
        print ("test_create_user : errors / ko")

    #assert response.json()["email"] == user_data["email"]

#______________________________________________________________________________
#
# region  start_uvicorn
#______________________________________________________________________________
async def start_uvicorn():
    config = uvicorn.Config("main:app", host="127.0.0.1", port=8000, reload=True)
    server = uvicorn.Server(config)
    
    # Démarrer le serveur
    await server.serve()

#______________________________________________________________________________
#
# region  stop_uvicorn
#______________________________________________________________________________
async def stop_uvicorn(server_task : asyncio.Task):
    server_task.cancel()  # Annuler la tâche du serveur Uvicorn
    try:
        await server_task  # Attendre que la tâche soit bien terminée
    except asyncio.CancelledError:
        pass  # Ignorer l'exception d'annulation


#______________________________________________________________________________
#
# region all_tests
#______________________________________________________________________________
async def all_tests() :

    # Créer et démarrer le serveur Uvicorn
    print("Start uvicorn server...")
    server_task = asyncio.create_task(start_uvicorn())
    
    # Attendre un peu pour que le serveur démarre (1 seconde)
    await asyncio.sleep(1)
 
    tests = []
    tests.append(test_login)
    tests.append(test_get_users)
    tests.append(test_create_user)
    tests.append(test_activation)
    tests.append(test_loans_history)
    tests.append(test_loans_request)
    tests.append(test_logout)

    # Faire les requêtes HTTP
    print("_________________________________________________________")
    for test in tests:
        await test()
        print("_________________________________________________________")

    # Après avoir effectué les tests, arrêter le serveur proprement
    print("Stop uvicorn server...")
    await stop_uvicorn(server_task)

    print("done.")

if __name__ == "__main__":
    asyncio.run(all_tests())


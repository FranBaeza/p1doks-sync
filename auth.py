import getpass

from pycognito.aws_srp import AWSSRP


POOL_ID = "ca-central-1_VGoFypwe"
CLIENT_ID = "6mu7svlaa4q8i1mvkeknhsruo8"
REGION = "ca-central-1"


class P1DoksAWSSRP(AWSSRP):

    def process_challenge(self, challenge_parameters, request_parameters):

        response = super().process_challenge(
            challenge_parameters,
            request_parameters
        )

        # P1Doks utiliza USER_ID_FOR_SRP como USERNAME
        # en el PASSWORD_VERIFIER challenge.
        user_id_for_srp = challenge_parameters["USER_ID_FOR_SRP"]

        response["USERNAME"] = user_id_for_srp

        return response


def authenticate():

    print("\n==============================")
    print("AUTENTICACIÓN P1DOKS")
    print("==============================")

    username = input("Usuario P1Doks: ")
    password = getpass.getpass("Contraseña P1Doks: ")

    print("\nIniciando sesión...")

    aws = P1DoksAWSSRP(
        username=username,
        password=password,
        pool_id=POOL_ID,
        client_id=CLIENT_ID,
        pool_region=REGION
    )

    response = aws.authenticate_user()

    authentication_result = response["AuthenticationResult"]

    access_token = authentication_result["AccessToken"]

    print("✓ Autenticación correcta")

    return {
        "username": username,
        "access_token": access_token
    }


if __name__ == "__main__":

    result = authenticate()

    print("\nLogin realizado correctamente.")
    print(f"Usuario: {result['username']}")
    print("Access token recibido: SI")
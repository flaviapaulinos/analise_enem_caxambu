from locust import HttpUser, task, between

class ENEMUser(HttpUser):

    wait_time = between(1, 3)

    @task
    def prever_nota(self):

        payload = {
            "SalMin": "3 a 5",
            "Escola": "privada",
            "OcupPaisMedia": 2.0,
            "EscolaridadePaisMedia": 3.0,
            "Cel": 2,
            "Comptdr": 1,
            "PessoasResd": 3
        }

        self.client.post("/predict", json=payload)
import secrets
import requests
from uuid import UUID

from app.models.sensor_node import TTNKeys
from app.config import settings

#https://github.com/TheThingsNetwork/lorawan-devices/blob/master/vendor/heltec/cubecell-dev-board-class-a-otaa.yaml

class TTNService:
    
    def __init__(self):
        self.app_id = settings.TTN_APP_ID
        api_key = settings.TTN_API_KEY
        
        self.base_url = f"https://eu1.cloud.thethings.network/api/v3"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    
    def create_device(self, sensor_node_id: UUID):
        device_id = str(sensor_node_id)
        dev_eui = self._random_hex(8)
        join_eui = "0000000000000000"
        app_key = self._random_hex(16)

        # === Schritt 1: Identity Server ===
        is_url = f"{self.base_url}/applications/{self.app_id}/devices"
        identity_payload = {
            "end_device": {
                "ids": {
                    "device_id": device_id,
                    "dev_eui": dev_eui,
                    "join_eui": join_eui
                },
                "supports_join": True
            },
            "field_mask": {
                "paths": [
                    "ids.device_id",
                    "ids.dev_eui",
                    "ids.join_eui",
                    "supports_join"
                ]
            }
        }

        is_resp = requests.post(is_url, json=identity_payload, headers=self.headers)
        if is_resp.status_code != 200:
            raise Exception(f"Identity Server error: {is_resp.status_code} – {is_resp.text}")

        # === Schritt 2: Join Server ===
        js_url = f"{self.base_url}/js/applications/{self.app_id}/devices/{device_id}"
        join_payload = {
            "end_device": {
                "ids": {
                    "device_id": device_id,
                    "dev_eui": dev_eui,
                    "join_eui": join_eui
                },
                "root_keys": {
                    "app_key": {
                        "key": app_key
                    }
                }
            },
            "field_mask": {
                "paths": [
                    "root_keys.app_key.key"
                ]
            }
        }

        js_resp = requests.put(js_url, json=join_payload, headers=self.headers)
        if js_resp.status_code != 200:
            raise Exception(f"Join Server error: {js_resp.status_code} – {js_resp.text}")

        # === Schritt 3: Network Server ===
        ns_url = f"{self.base_url}/ns/applications/{self.app_id}/devices/{device_id}"
        ns_payload = {
            "end_device": {
                "lorawan_version": "MAC_V1_0_2",
                "frequency_plan_id": "EU_863_870"
            },
            "field_mask": {
                "paths": [
                    "lorawan_version",
                    "frequency_plan_id"
                ]
            }
        }

        ns_resp = requests.put(ns_url, json=ns_payload, headers=self.headers)
        if ns_resp.status_code != 200:
            raise Exception(f"Network Server error: {ns_resp.status_code} – {ns_resp.text}")

        return TTNKeys(
            app_key=app_key,
            dev_eui=dev_eui,
            join_eui=join_eui
        )
    def delete_device(self, sensor_node_id: UUID):
        url = f"{self.base_url}/devices/{sensor_node_id}"
        response = requests.delete(url, headers=self.headers)
        if response.status_code == 204:
            print("Deleted device successfully")
            #return {"status": "deleted", "device_id": device_id}
        else:
            response.raise_for_status()
    
    def _random_hex(self, length_bytes: int) -> str:
        return secrets.token_hex(length_bytes).upper()
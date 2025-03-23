# ai_comms.py
import requests
import json
import uuid
import time
import socket
from datetime import datetime

class AICommsProtocol:
    def __init__(self, team_id="baja_boys", host="localhost", port=5000):
        self.team_id = team_id
        self.host = host
        self.port = port
        self.peers = {}  # Store known AI peers
        self.conversation_history = {}
        
    def generate_message(self, target_id, message_type, content_type, payload, metadata=None):
        """Create a structured message in the protocol format"""
        conversation_id = str(uuid.uuid4())[:8]
        
        message = {
            "header": {
                "source_id": self.team_id,
                "target_id": target_id,
                "message_type": message_type,
                "timestamp": datetime.now().isoformat(),
                "conversation_id": conversation_id,
                "protocol_version": "1.0"
            },
            "body": {
                "content_type": content_type,
                "payload": payload,
                "metadata": metadata or {}
            }
        }
        
        # Store in conversation history
        self.conversation_history[conversation_id] = {
            "sent": message,
            "timestamp": datetime.now().isoformat()
        }
        
        return message, conversation_id
    
    def send_message(self, target_id, message_type, content_type, payload, metadata=None):
        """Send a message to another AI"""
        if target_id not in self.peers and target_id != "b2_cloud":
            return {"error": "Unknown peer"}
        
        message, conversation_id = self.generate_message(
            target_id, message_type, content_type, payload, metadata
        )
        
        # Determine endpoint based on target
        if target_id == "b2_cloud":
            endpoint = "https://biosphere2.org/research/systems-data/api/reason"
            headers = {"Authorization": "Bearer hackathon:99](uM6"}
        else:
            endpoint = f"http://{self.peers[target_id]['host']}:{self.peers[target_id]['port']}/receive"
            headers = {}
        
        try:
            response = requests.post(endpoint, json=message, headers=headers)
            
            # Store response in conversation history
            if response.status_code == 200:
                self.conversation_history[conversation_id]["received"] = response.json()
                self.conversation_history[conversation_id]["completed"] = datetime.now().isoformat()
                
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def discover_peers(self, subnet="192.168.1"):
        """Scan the network for other AIs running the protocol"""
        discovered = {}
        
        # For the hackathon, a simple approach to discover peers
        for i in range(1, 255):
            try:
                ip = f"{subnet}.{i}"
                response = requests.get(f"http://{ip}:5000/discover", timeout=0.5)
                if response.status_code == 200:
                    peer_data = response.json()
                    if "team_id" in peer_data and peer_data["team_id"] != self.team_id:
                        discovered[peer_data["team_id"]] = {
                            "host": ip,
                            "port": 5000,
                            "capabilities": peer_data.get("capabilities", [])
                        }
                        # Add to known peers
                        self.peers[peer_data["team_id"]] = {
                            "host": ip,
                            "port": 5000
                        }
            except:
                continue
                
        return discovered
    
    def register_with_b2_cloud(self):
        """Register this AI with the B2 cloud model"""
        try:
            # Get the machine's IP address
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            registration_data = {
                "header": {
                    "source_id": self.team_id,
                    "target_id": "b2_cloud",
                    "message_type": "register",
                    "timestamp": datetime.now().isoformat(),
                    "protocol_version": "1.0"
                },
                "body": {
                    "content_type": "registration",
                    "payload": {
                        "team_id": self.team_id,
                        "ip": local_ip,
                        "port": self.port,
                        "model": "mistral-local",
                        "capabilities": ["csv_analysis", "time_series"]
                    }
                }
            }
            
            response = requests.post(
                "https://biosphere2.org/research/systems-data/api/register",
                json=registration_data,
                headers={"Authorization": "Bearer hackathon:99](uM6"}
            )
            
            return response.json()
        except Exception as e:
            return {"error": str(e)}
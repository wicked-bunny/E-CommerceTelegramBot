# infrastructure/ngrok_tunnel.py
import os
from pyngrok import ngrok


class NgrokTunnelManager:
    @staticmethod
    def start_tunnel(port: int = 5000):
        """
        Initializes and starts a secure public ngrok tunnel bound to the local port.
        Authenticates via the NGROK_AUTH_TOKEN environment variable.
        """
        # Match the exact naming convention from your BotToken.env file
        authtoken = os.getenv("NGROK_AUTH_TOKEN")
        if not authtoken:
            raise ValueError("❌ NGROK_AUTH_TOKEN is missing in your environment configuration.")

        # Enforce authentication credentials before session creation
        ngrok.set_auth_token(authtoken)

        # Open the network proxy bridge
        tunnel = ngrok.connect(port)

        print(f"\n🚀 [NGROK] SECURITY TUNNEL ACTIVATED SUCCESSFULLY!")
        print(f"🔗 Public Destination URL for your Stripe Dashboard:")
        print(f"   👉 \033[94m{tunnel.public_url}/stripe_webhook\033[0m 👈")
        print(
            f"⚠️  Copy the blue link above, paste it into Developers -> Webhooks, and subscribe to 'checkout.session.completed'\n")

        return tunnel

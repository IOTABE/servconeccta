import os
import requests
from django.conf import settings
from typing import Optional


class WhatsAppService:
    """Serviço de integração com WhatsApp Business API (Meta)"""

    def __init__(self):
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
        self.business_account_id = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
        self.api_url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"

    def _get_headers(self) -> dict:
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
        }

    def send_contact_message(
        self,
        phone: str,
        professional_name: str,
        client_name: str,
        service_title: str,
        message_type: str = 'contact_request'
    ) -> dict:
        """
        Envia mensagem de contato via WhatsApp para profissional.
        Usado quando cliente deseja entrar em contato com profissional.
        """

        templates = {
            'contact_request': {
                'type': 'contact_request',
                'first_name': professional_name.split()[0],
                'client_name': client_name,
                'service': service_title,
            }
        }

        template = templates.get(message_type, templates['contact_request'])

        payload = {
            'messaging_product': 'whatsapp',
            'to': self._format_phone(phone),
            'type': 'template',
            'template': {
                'name': 'contact_notification',
                'language': {'code': 'pt_BR'},
                'components': [
                    {
                        'type': 'body',
                        'parameters': [
                            {'type': 'text', 'parameter_name': 'professional_name', 'text': template['first_name']},
                            {'type': 'text', 'parameter_name': 'client_name', 'text': template['client_name']},
                            {'type': 'text', 'parameter_name': 'service_title', 'text': template['service']},
                        ]
                    }
                ]
            }
        }

        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except requests.RequestException as e:
            return {'success': False, 'error': str(e)}

    def send_direct_message(
        self,
        phone: str,
        message: str,
        preview_url: Optional[str] = None
    ) -> dict:
        """Envia mensagem direta via WhatsApp"""

        payload = {
            'messaging_product': 'whatsapp',
            'to': self._format_phone(phone),
            'type': 'text',
            'text': {'body': message}
        }

        if preview_url:
            payload['type'] = 'interactive'
            payload['interactive'] = {
                'type': 'button',
                'body': {'text': message},
                'action': {
                    'buttons': [
                        {'type': 'reply', 'reply': {'id': 'view_details', 'title': 'Ver Detalhes'}, 'url': preview_url}
                    ]
                }
            }

        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except requests.RequestException as e:
            return {'success': False, 'error': str(e)}

    def _format_phone(self, phone: str) -> str:
        """Formata número para formato WhatsApp (55+DDD+numero)"""
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) == 10:
            digits = '55' + digits
        elif len(digits) == 11 and digits[0] == '0':
            digits = '55' + digits[1:]
        elif len(digits) == 11:
            digits = '55' + digits
        return digits

    def _handle_response(self, response: requests.Response) -> dict:
        if response.status_code in [200, 201]:
            data = response.json()
            return {
                'success': True,
                'message_id': data.get('messages', [{}])[0].get('id')
            }
        return {
            'success': False,
            'error': response.json().get('error', {}).get('message', 'Unknown error'),
            'code': response.status_code
        }


def get_whatsapp_link(phone: str, message: str = '') -> str:
    """Gera link direto para WhatsApp Web/App"""
    phone_formatted = ''.join(filter(str.isdigit, phone))
    encoded_message = requests.utils.quote(message)
    return f"https://wa.me/{phone_formatted}?text={encoded_message}"
import json
import platform
import logging
import requests
from spiderling.sistema import Sistema


class Logger():
    """
    Classe Logger que define os loggers da Konker
    """
    def __init__(self, dispositivoKonker, usuarioKonker, senhaKonker, url_konker_pub):
        """
        Função construtora da classe Logger
        """
        self._logger = logging.getLogger(__name__)
        self.dispositivoKonker = dispositivoKonker
        self.usuarioKonker = usuarioKonker
        self.senhaKonker = senhaKonker
        self.url_konker_pub = url_konker_pub

    def registrarHealth(self):
        """
        Função que realiza o registro do log do Health
        """
        self._logger.info("Comando registraHealth inicializado")
        try:
            sistema = Sistema()
            memoria_perc, memoria_usada = sistema.pegarMemoria()
            swap_perc, swap_usada = sistema.pegarSwap()
            disco = sistema.pegarDiscos()
            # disco = 'N/D - Windows'
            hostname = platform.uname()[1]  # os.uname()[1]
            ip = sistema.pegarIPs()
            # timestamp = datetime.datetime.now().timestamp()
            url = self.url_konker_pub + self.usuarioKonker + "/health"
            headers = {'content-type': 'application/json', 'Accept': 'application/json'}
            auth = (self.usuarioKonker, self.senhaKonker)

            # ## GERAL
            msg = {
                "id": self.dispositivoKonker,
                "health": 1,
                "host": {
                    "name": hostname,
                    "ip": ip,
                    "memory": {
                        "perc": memoria_perc,
                        "mb": memoria_usada
                    },
                    "cpu": sistema.pegarCPU(),
                    "swap": {
                        "perc": swap_perc,
                        "mb": swap_usada
                    },
                    "disks": disco
                }
            }

            requests.post(url, headers=headers, auth=auth, data=json.dumps(msg))

            self._logger.info("Comando registraHealth finalizado")
            return True
        except Exception as e:
            self._logger.error(f'erro: {str(e)}')
            return e

    def registrarExecucao(self, nome_operacao, id, duracao, mensagem, erro, codigo_erro):
        """
        Função que realiza o registro da execução da operação
        """
        self._logger.info("Comando registraExecucao inicializado")
        try:
            url = self.url_konker_pub + self.usuarioKonker + "/log"
            headers = {'content-type': 'application/json', 'Accept': 'application/json'}
            auth = (self.usuarioKonker, self.senhaKonker)

            # ## GERAL
            if not erro:
                msg = {"action": nome_operacao, "id": id, "status": 'sucess', "message": mensagem, "duration": duracao, }
            else:
                msg = {"action": nome_operacao, "id": id, "status": 'failure', "message": str(f'error : {str(codigo_erro)} - {mensagem}')}
            requests.post(url, headers=headers, auth=auth, data=json.dumps(msg))

            self._logger.info("Comando registraExecucao finalizado")
            return True
        except Exception as e:
            self._logger.error(f'erro: {str(e)}')
            return e

    def registrarCiencia(self, nome_operacao, id):
        """
        Função que registra a confirmação de recebimento do comando
        """
        self._logger.info("Comando registraCiencia inicializado")
        try:
            url = f'{self.url_konker_pub}{self.usuarioKonker}/ack'
            headers = {'content-type': 'application/json', 'Accept': 'application/json'}
            auth = (self.usuarioKonker, self.senhaKonker)

            # ## GERAL
            msg = {'type': 'ack', "action": nome_operacao, "id": id}
            requests.post(url, headers=headers, auth=auth, data=json.dumps(msg))

            self._logger.info("Comando registraCiencia finalizado")
            return True
        except Exception as e:
            self._logger.error(f'erro: {str(e)}')
            return e

    def registrar_report(self, id, msg_report):
        """
        Função que registra a mensagem de report
        """
        self._logger.info("Comando registraReport inicializado")
        try:
            url = f'{self.url_konker_pub}{self.usuarioKonker}/report'
            headers = {'content-type': 'application/json', 'Accept': 'application/json'}
            auth = (self.usuarioKonker, self.senhaKonker)

            # ## GERAL
            msg = {'type': 'report', 'id': id, 'msg': msg_report}
            requests.post(url, headers=headers, auth=auth, data=json.dumps(msg))

            self._logger.info("Comando registraReport finalizado")
            return True
        except Exception as e:
            self._logger.error(f'erro: {str(e)}')
            return e

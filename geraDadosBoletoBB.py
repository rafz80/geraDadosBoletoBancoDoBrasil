
# ---------------------------
# Script para geração de dados para boleto do Banco do Brasil
# Conforme manual que me foi enviado em Setembro de 2020
# Algumas explicações no corpo do código
# Boa sorte!
# ---------------------------


import requests
import urllib3
import xml.etree.ElementTree as ET


# biblioteca para desabilitar os warnings por conta do SSL vencido do ambiente de homologacao
urllib3.disable_warnings()

headers = { 'Content-Type': 'application/x-www-form-urlencoded', 
			'Authorization': 'Basic ZXlKcFpDSTZJamd3TkROaU5UTXRaalE1TWkwMFl5SXNJbU52WkdsbmIxQjFZbXhwWTJGa2IzSWlPakV3T1N3aVkyOWthV2R2VTI5bWRIZGhjbVVpT2pFc0luTmxjWFZsYm1OcFlXeEpibk4wWVd4aFkyRnZJam94ZlE6ZXlKcFpDSTZJakJqWkRGbE1HUXROMlV5TkMwME1HUXlMV0kwWVNJc0ltTnZaR2xuYjFCMVlteHBZMkZrYjNJaU9qRXdPU3dpWTI5a2FXZHZVMjltZEhkaGNtVWlPakVzSW5ObGNYVmxibU5wWVd4SmJuTjBZV3hoWTJGdklqb3hMQ0p6WlhGMVpXNWphV0ZzUTNKbFpHVnVZMmxoYkNJNk1YMA==',
			'Cache-Control': 'no-cache',
			'Host': 'https://oauth.hm.bb.com.br/oauth/token' }



params = "grant_type=client_credentials&scope=cobranca.registro-boletos "
URL = "https://oauth.hm.bb.com.br/oauth/token"
r = requests.post(URL, data=params, headers=headers)
resultado = r.json()



token = "Bearer " + resultado['access_token']


headersXML = {  'Content-Type': 'text/xml',
				'SOAPACTION': 'registrarBoleto',
				'Authorization': token }



# abaixo, xml de exemplo existente no manual da API do Banco do Brasil
# monte seu XML com os dados do seu convênio e cliente

xml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:sch="http://www.tibco.com/schemas/bws_registro_cbr/Recursos/XSD/Schema.xsd">
 <soapenv:Header/>
 <soapenv:Body>
 <sch:requisicao>
 <sch:numeroConvenio>2625444</sch:numeroConvenio>
 <sch:numeroCarteira>17</sch:numeroCarteira>
 <sch:numeroVariacaoCarteira>19</sch:numeroVariacaoCarteira>
 <sch:codigoModalidadeTitulo>1</sch:codigoModalidadeTitulo>
 <sch:dataEmissaoTitulo>01.03.2020</sch:dataEmissaoTitulo>
 <sch:dataVencimentoTitulo>21.11.2020</sch:dataVencimentoTitulo>
 <sch:valorOriginalTitulo>30000</sch:valorOriginalTitulo>
 <sch:codigoTipoDesconto>1</sch:codigoTipoDesconto>
 <sch:dataDescontoTitulo>21.11.2019</sch:dataDescontoTitulo>
 <sch:percentualDescontoTitulo/>
 <sch:valorDescontoTitulo>10</sch:valorDescontoTitulo>
 <sch:valorAbatimentoTitulo/>
 <sch:quantidadeDiaProtesto>0</sch:quantidadeDiaProtesto>
 <sch:codigoTipoJuroMora>0</sch:codigoTipoJuroMora>
 <sch:percentualJuroMoraTitulo/>
 <sch:valorJuroMoraTitulo/>
 <sch:codigoTipoMulta>2</sch:codigoTipoMulta>
 <sch:dataMultaTitulo>22.11.2020</sch:dataMultaTitulo>
 <sch:percentualMultaTitulo>10</sch:percentualMultaTitulo>
 <sch:valorMultaTitulo/>
 <sch:codigoAceiteTitulo>N</sch:codigoAceiteTitulo>
 <sch:codigoTipoTitulo>2</sch:codigoTipoTitulo>
 <sch:textoDescricaoTipoTitulo>DUPLICATA</sch:textoDescricaoTipoTitulo>
 <sch:indicadorPermissaoRecebimentoParcial>N</sch:indicadorPermissaoRecebimentoParcial>
 <sch:textoNumeroTituloBeneficiario>987654321987654</sch:textoNumeroTituloBeneficiario>
 <sch:textoCampoUtilizacaoBeneficiario/>
 <sch:codigoTipoContaCaucao>1</sch:codigoTipoContaCaucao>
 <sch:textoNumeroTituloCliente>00026254440000000102</sch:textoNumeroTituloCliente>
 <sch:textoMensagemBloquetoOcorrencia>Pagamento disponivel ate a data de vencimento</sch:textoMensagemBloquetoOcorrencia>
 <sch:codigoTipoInscricaoPagador>2</sch:codigoTipoInscricaoPagador>
 <sch:numeroInscricaoPagador>00000000000191</sch:numeroInscricaoPagador>
 <sch:nomePagador>MERCADO TESTE</sch:nomePagador>
 <sch:textoEnderecoPagador>RUA SEM NOME</sch:textoEnderecoPagador>
 <sch:numeroCepPagador>12345678</sch:numeroCepPagador>
 <sch:nomeMunicipioPagador>BRASILIA</sch:nomeMunicipioPagador>
 <sch:nomeBairroPagador>SIA</sch:nomeBairroPagador>
 <sch:siglaUfPagador>DF</sch:siglaUfPagador>
 <sch:textoNumeroTelefonePagador>45619988</sch:textoNumeroTelefonePagador>
 <sch:codigoTipoInscricaoAvalista/>
 <sch:numeroInscricaoAvalista/>
 <sch:nomeAvalistaTitulo/>
 <sch:codigoChaveUsuario>1</sch:codigoChaveUsuario>
 <sch:codigoTipoCanalSolicitacao>5</sch:codigoTipoCanalSolicitacao>
 </sch:requisicao>
 </soapenv:Body>
</soapenv:Envelope> """


# requesta o XML por POST
response = requests.post('https://cobranca.homologa.bb.com.br:7101/registrarBoleto', verify=False, data=xml, headers=headersXML)

if response.status_code == 200:
	
	payload = ET.fromstring(response.text)
	for node in payload.iter():
				
		print(node.tag.replace('{http://www.tibco.com/schemas/bws_registro_cbr/Recursos/XSD/Schema.xsd}', '') + ' - ' + str(node.text))
		
		# pegue as informações e monte seu boleto


else:
	print("Ocorreu um erro na comunicação com o BB, por favor tente mais tarde!")
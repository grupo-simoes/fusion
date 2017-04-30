import simplejson as json
import webbrowser
import httplib2
import wx

from apiclient import discovery
from oauth2client import client
from apiclient.discovery import build
from apiclient.discovery import build
from wx.lib import sheet

class Model:
    def __init__(self):
        self.flow = client.flow_from_clientsecrets(
            'client_secrets.json',
            scope='https://www.googleapis.com/auth/fusiontables',
            redirect_uri='urn:ietf:wg:oauth:2.0:oob')

        self.auth_uri = self.flow.step1_get_authorize_url()
        webbrowser.open(self.auth_uri)

    def abreConexao(self, codigoAutorizacao):
        self.credenciais = self.flow.step2_exchange(codigoAutorizacao)
        self.http_auth = self.credenciais.authorize(httplib2.Http())
        self.fusionService =  discovery.build('fusiontables', 'v2'	, self.http_auth)


class Painel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

class Folha(sheet.CSheet):
    def __init__(self, parent, colunas, linhas):
        sheet.CSheet.__init__(self, parent)
        self.row = self.col = 0
        self.SetNumberRows(colunas)
        self.SetNumberCols(linhas)

        for i in range(colunas):
            self.SetRowSize(i, 20)


class Tela(wx.Frame):
    def __init__(self, parent , estilo, titulo, icone, comprimento, largura):
        super(Tela, self).__init__(parent,  style=estilo, title=titulo, size = (comprimento, largura))
        self.Painel = Painel(self)

        self.CreateStatusBar()
        self.Centre()

        if icone:
            icon = wx.EmptyIcon()
            icon.CopyFromBitmap(wx.Bitmap(icone, wx.BITMAP_TYPE_ANY))
            self.SetIcon(icon)

    def __del__( self ):
        pass

class TelaLogin:
    def __init__(self):
        self.Tela = Tela(None, wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER,'Login', '', 220, 340)

        self.InitUI()
        self.Tela.Centre()
        self.Tela.MakeModal()
        self.Tela.Show()

    def InitUI(self):
        self.LogoTipo = wx.StaticBitmap(self.Tela.Painel,size=(200,200))
        self.LogoTipo.SetBitmap(wx.Bitmap('PNG/logo.png'))

        self.Rotulo1 = wx.StaticText( self.Tela.Painel, label='Usuario')
        self.Rotulo2 = wx.StaticText( self.Tela.Painel, label='Senha')

        self.CaixaTexto1 = wx.TextCtrl(self.Tela.Painel)
        self.CaixaTexto2 = wx.TextCtrl(self.Tela.Painel)

        self.BotaoOk = wx.Button(self.Tela.Painel, label='Ok')
        self.BotaoCancelar = wx.Button(self.Tela.Painel, label='Cancelar')

        self.Tela.Bind(wx.EVT_BUTTON, self.AoClickBotaoOk, self.BotaoOk)
        self.Tela.Bind(wx.EVT_BUTTON, self.AoClickBotaoCancelar, self.BotaoCancelar)

        self.MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.ImageSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.GridSizer = wx.GridBagSizer(4, 4)

        self.ImageSizer.Add(self.LogoTipo, 0, wx.ALL, 5)

        self.GridSizer.Add(self.Rotulo1, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        self.GridSizer.Add(self.CaixaTexto1, pos=(0, 1), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)
        self.GridSizer.Add(self.Rotulo2, pos=(1, 0),  flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        self.GridSizer.Add(self.CaixaTexto2, pos=(1, 1), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)
        self.GridSizer.Add(self.BotaoOk, pos=(2, 0), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)
        self.GridSizer.Add(self.BotaoCancelar, pos=(2, 1), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)

        self.MainSizer.Add(self.ImageSizer, 0, wx.CENTER)
        self.MainSizer.Add(wx.StaticLine(self.Tela.Painel,), 0, wx.ALL|wx.EXPAND, 5)
        self.MainSizer.Add(self.GridSizer, 0, wx.ALL|wx.EXPAND, 5)

        self.Tela.Painel.SetSizer(self.MainSizer)
        self.Tela.Painel.Layout()


    def AoClickBotaoOk(self, event):
        self.BotaoOk = event.GetEventObject()
        print '\n botao ok'


    def AoClickBotaoCancelar(self, event):
        self.BotaoCancelar = event.GetEventObject()
        print '\n botao Cancelar'

class TelaAutorizacao:
    def __init__(self):
        self.Tela = Tela(None, wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER,'Autorizacao', '', 320, 140)

        self.InitUI()
        self.Tela.Centre()
        self.Tela.Show()

    def InitUI(self):
        self.Rotulo = wx.StaticText( self.Tela.Painel, label='Autorizacao')

        self.CaixaTexto = wx.TextCtrl(self.Tela.Painel)

        self.BotaoOk =  wx.Button(self.Tela.Painel, label='Ok')
        self.BotaoCancelar =  wx.Button(self.Tela.Painel, label='Cancelar')

        self.Tela.Bind(wx.EVT_BUTTON, self.AoClickBotaoOk, self.BotaoOk)
        self.Tela.Bind(wx.EVT_BUTTON, self.AoClickBotaoCancelar, self.BotaoCancelar)

        self.MainSizer = wx.GridBagSizer(4, 4)

        self.MainSizer.Add(self.Rotulo, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        self.MainSizer.Add(self.CaixaTexto, pos=(1, 0), span=(1, 5),flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)
        self.MainSizer.Add(self.BotaoOk, pos=(3, 3), flag=wx.RIGHT|wx.BOTTOM, border=5)
        self.MainSizer.Add(self.BotaoCancelar, pos=(3, 4), flag=wx.RIGHT|wx.BOTTOM, border=5)

        self.Tela.Painel.SetSizer(self.MainSizer)
        self.Tela.Painel.Layout()

    def AoClickBotaoOk(self, event):
        self.BotaoOk = event.GetEventObject()
        print '\n botao ok'


    def AoClickBotaoCancelar(self, event):
        self.BotaoCancelar = event.GetEventObject()
        print '\n botao Cancelar'

class TelaMenu:
    def __init__(self):
        self.Tela = Tela(None, wx.DEFAULT_FRAME_STYLE,"Sistema", "", 550, 500)

        self.InitUI()
        self.Tela.Centre()
        self.Tela.Show()
        self.Tela.Maximize(True)

    def InitUI(self):
        self.BitMapClientes = wx.Bitmap("PNG/botao_cliente.png", wx.BITMAP_TYPE_ANY)
        self.BitMapFornecedores = wx.Bitmap("PNG/botao_fornec.png", wx.BITMAP_TYPE_ANY)
        self.BitMapOSRelatorios = wx.Bitmap("PNG/botao_os_rel.png", wx.BITMAP_TYPE_ANY)
        self.BitMapFinanceiro = wx.Bitmap("PNG/botao_financeiro.png", wx.BITMAP_TYPE_ANY)
        self.BitMapOrcarmeto = wx.Bitmap("PNG/botao_os_rel.png", wx.BITMAP_TYPE_ANY)
        self.BitMapConfiguracoes = wx.Bitmap("PNG/botao_config.png", wx.BITMAP_TYPE_ANY)
        self.BitMapSair = wx.Bitmap("PNG/botao_sair.png", wx.BITMAP_TYPE_ANY)

        self.BotaoClients = wx.BitmapButton(self.Tela.Painel, id = wx.ID_ANY, bitmap=self.BitMapClientes)
        self.BotaoFornecedores = wx.BitmapButton(self.Tela.Painel, id = wx.ID_ANY, bitmap=self.BitMapFornecedores   )
        self.BotaoOSRelatorios = wx.BitmapButton(self.Tela.Painel, id = wx.ID_ANY, bitmap=self.BitMapOSRelatorios)
        self.BotaoFinanceiro = wx.BitmapButton(self.Tela.Painel, id = wx.ID_ANY, bitmap=self.BitMapFinanceiro)
        self.BotaoOrcarmeto = wx.BitmapButton(self.Tela.Painel, id = wx.ID_ANY, bitmap=self.BitMapOrcarmeto)
        self.BotaoConfiguracoes = wx.BitmapButton(self.Tela.Painel, id = wx.ID_ANY, bitmap=self.BitMapConfiguracoes)
        self.BotaoSair = wx.Button = wx.BitmapButton(self.Tela.Painel, id = wx.ID_ANY, bitmap=self.BitMapSair)


        self.Tela.Bind(wx.EVT_BUTTON, self.AoClickBotaoCliente, self.BotaoClients)
        self.Tela.Bind(wx.EVT_BUTTON, self.AoClickBotaoFornecedores, self.BotaoFornecedores)
        self.Tela.Bind(wx.EVT_BUTTON, self.AoClickBotaoOSRelatorio, self.BotaoOSRelatorios)
        self.Tela.Bind(wx.EVT_BUTTON, self.AoClickBotaoFinanceiro, self.BotaoFinanceiro)
        self.Tela.Bind(wx.EVT_BUTTON, self.AoClickBotaoOrcamento, self.BotaoOrcarmeto)
        self.Tela.Bind(wx.EVT_BUTTON, self.AoClickBotaoConfiguracoes, self.BotaoConfiguracoes)
        self.Tela.Bind(wx.EVT_BUTTON, self.AoClickBotaoSair, self.BotaoSair)

        self.GridSizer = wx.GridSizer(3, 3, 5, 5)
        self.MainSizer = wx.BoxSizer(wx.VERTICAL)

        self.GridSizer.AddMany([(self.BotaoClients, 0 , wx.EXPAND),
                                      (self.BotaoFornecedores, 0 , wx.EXPAND),
                                      (self.BotaoOSRelatorios, 0 , wx.EXPAND),
                                      (self.BotaoFinanceiro, 0 , wx.EXPAND),
                                      (self.BotaoOrcarmeto, 0 , wx.EXPAND),
                                      (self.BotaoConfiguracoes, 0 , wx.EXPAND),
                                      (wx.StaticText(self.Tela.Painel), wx.EXPAND),
                                      (self.BotaoSair, 0 , wx.EXPAND)])

        self.MainSizer.Add((0,0), 1, wx.EXPAND)
        self.MainSizer.Add(self.GridSizer, 0, wx.CENTER)
        self.MainSizer.Add((0,0), 1, wx.EXPAND)

        self.Tela.Painel.SetSizer(self.MainSizer)


    def AoClickBotaoCliente(self, e):
        self.TelaCliente = TelaClientes()

    def AoClickBotaoFornecedores(self, e):
        self.TelaFornecedores = TelaFornecedores()

    def AoClickBotaoOSRelatorio(self, e):
        self.TelaOSRelatorio = TelaOrdemServicos()

    def AoClickBotaoFinanceiro(self, e):
        self.TelaOSRelatorio = TelaControleFinanceiro()

    def AoClickBotaoOrcamento(self, e):
        TelaOrcamentos()

    def AoClickBotaoConfiguracoes(self, e):
        TelaConfiguracao()

    def AoClickBotaoSair(self, e):
        self.Close()

class TelaConfiguracao:
    def __init__(self):
        self.Tela = Tela(None, wx.DEFAULT_FRAME_STYLE,"Configuracoes", "", 550, 500)

        self.Tela.Centre()
        self.Tela.Show()

class TelaControleFinanceiro:
    def __init__(self):
        self.Tela = Tela(None, wx.DEFAULT_FRAME_STYLE,"Financeiro", "", 550, 500)

        self.Tela.Centre()
        self.Tela.Show()

class TelaOrdemServicos:
    def __init__(self):
        self.Tela = Tela(None, wx.DEFAULT_FRAME_STYLE,"Ordens de Servico", "", 550, 500)

        self.Tela.Centre()
        self.Tela.Show()

class TelaOrcamentos:
    def __init__(self):
        self.Tela = Tela(None, wx.DEFAULT_FRAME_STYLE,"Orcamentos", "", 550, 500)

        self.Tela.Centre()
        self.Tela.Show()

class TelaFornecedores:
    def __init__(self):
        self.Tela = Tela(None, wx.DEFAULT_FRAME_STYLE,"Fornecedores", "", 550, 500)

        self.Tela.Centre()
        self.Tela.Show()

class TelaClientes:
    def __init__(self):
        self.Tela = Tela(None, wx.DEFAULT_FRAME_STYLE,"Clientes", "", 550, 500)

        self.InitUI()
        self.Tela.Centre()
        self.Tela.Show()

    def InitUI(self):
        self.GroupBoxPesquisa = wx.StaticBox(self.Tela.Painel, -1, 'Pesquisa')
        self.GroupBoxSizerPesquisa = wx.StaticBoxSizer(self.GroupBoxPesquisa, wx.HORIZONTAL)
        self.GroupPesquisaSizer = wx.GridBagSizer(2, 2)

        self.ImageCliente = wx.StaticBitmap(self.Tela.Painel,size=(80,80))
        self.ImageCliente.SetBitmap(wx.Bitmap('PNG/botao_cliente.png'))

        self.BitMapSair = wx.Bitmap("PNG/botao_sair.png", wx.BITMAP_TYPE_ANY)

        self.BotaoSair = wx.Button = wx.BitmapButton(self.Tela.Painel, id = wx.ID_ANY, bitmap=self.BitMapSair)

        self.MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.TitleSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ImageSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.GridSizer = wx.GridBagSizer(4, 4)

        self.ImageSizer.Add(self.ImageCliente, 0, wx.ALL)
        self.TitleSizer.Add(self.ImageSizer, 0, wx.LEFT)
        self.TitleSizer.Add(self.GroupBoxSizerPesquisa, 2, wx.CENTER|wx.EXPAND)
        self.TitleSizer.Add(self.BotaoSair, 0, wx.RIGHT)

        self.MainSizer.Add(self.TitleSizer, 0, wx.ALL|wx.EXPAND, 5)
        self.MainSizer.Add(wx.StaticLine(self.Tela.Painel,), 0, wx.ALL|wx.EXPAND, 5)
        self.MainSizer.Add(self.GridSizer, 0, wx.ALL|wx.EXPAND, 5)

        self.Tela.Painel.SetSizer(self.MainSizer)
        self.Tela.Painel.Layout()

class View:
    def __init__(self):
        #self.TelaMenu = TelaMenu()
        #self.TelaLogin = TelaLogin()
        #self.TelaAutorizacao = TelaAutorizacao()
        self.TelaCliente = TelaClientes()
class Controller:
    def __init__(self, app):
        self.view = View()
        #self.model = Model()

if __name__ == "__main__":
    app = wx.App()
    controller = Controller(app)
    app.MainLoop()

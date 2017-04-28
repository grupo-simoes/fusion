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
        self.Tela = Tela(None, wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER,'Login', '', 200, 400)

        self.InitUI()
        self.Tela.Centre()
        self.Tela.MakeModal()
        self.Tela.Show()

    def InitUI(self):
        self.LogoTipo = wx.StaticBitmap(self.Tela.Painel,size=(200,200))
        self.LogoTipo.SetBitmap(wx.Bitmap('PNG/logo.pnj'))

        self.Rotulo1 = wx.StaticText( self.Tela.Painel, label='Usuario')
        self.Rotulo2 = wx.StaticText( self.Tela.Painel, label='Senha')

        self.CaixaTexto1 = wx.TextCtrl(self.Tela.Painel)
        self.CaixaTexto2 = wx.TextCtrl(self.Tela.Painel)

        self.BotaoOk = wx.Button(self.Tela.Painel, label='Ok')
        self.BotaoCancelar = wx.Button(self.Tela.Painel, label='Cancelar')

        self.Tela.Bind(wx.EVT_BUTTON, self.AoClickBotaoOk, self.BotaoOk)
        self.Tela.Bind(wx.EVT_BUTTON, self.AoClickBotaoCancelar, self.BotaoCancelar)

        self.ConstroiSizers()


    def ConstroiSizers(self):
        self.MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SizerTitle = wx.BoxSizer(wx.HORIZONTAL)
        self.SizerLineOne = wx.BoxSizer(wx.HORIZONTAL)
        self.SizerLineTwo = wx.BoxSizer(wx.HORIZONTAL)
        self.SizerLineThree = wx.BoxSizer(wx.HORIZONTAL)

        self.SizerTitle.Add(self.LogoTipo, 0, wx.ALL, 5)
        self.SizerLineOne.Add(self.Rotulo1, 0, wx.ALL|wx.EXPAND, 5)
        self.SizerLineOne.Add(self.CaixaTexto1, 0 ,wx.ALL|wx.EXPAND, 5)
        self.SizerLineTwo.Add(self.Rotulo2, 0 ,wx.ALL, 5)
        self.SizerLineTwo.Add(self.CaixaTexto2, 0 ,wx.ALL, 5)
        self.SizerLineThree.Add(self.BotaoOk, 0, wx.ALL, 5)
        self.SizerLineThree.Add(self.BotaoCancelar, 0, wx.ALL, 5)

        self.MainSizer.Add(self.SizerTitle, 0 ,wx.Center)
        self.MainSizer.Add(wx.StaticLine(self.Tela.Painel,), 0, wx.ALL|wx.EXPAND, 5)
        self.MainSizer.Add(self.SizerLineOne, 0, wx.ALL|wx.EXPAND, 5)
        self.MainSizer.Add(self.SizerLineTwo, 0, wx.ALL|wx.EXPAND, 5)
        self.MainSizer.Add(self.SizerLineThree, 0, wx.ALL|wx.EXPAND, 5)
        self.MainSizer.Add(wx.StaticLine(self.Tela.Painel,), 0, wx.ALL|wx.EXPAND, 5)

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

        self.ConstroiSizers()

    def ConstroiSizers(self):
        self.MainSizer = wx.GridBagSizer(4, 4)

        self.MainSizer.Add(self.Rotulo, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        self.MainSizer.Add(self.CaixaTexto, pos=(1, 0), span=(1, 5),flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)
        self.MainSizer.Add(self.BotaoOk, pos=(3, 3))
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
        self.BitMapClientes = wx.Bitmap("PNG/ClientsSmall.png", wx.BITMAP_TYPE_ANY)
        self.BitMapFornecedores = wx.Bitmap("PNG/ClientsSmall.png", wx.BITMAP_TYPE_ANY)
        self.BitMapOSRelatorios = wx.Bitmap("PNG/ClientsSmall.png", wx.BITMAP_TYPE_ANY)
        self.BitMapFinanceiro = wx.Bitmap("PNG/ClientsSmall.png", wx.BITMAP_TYPE_ANY)
        self.BitMapOrcarmeto = wx.Bitmap("PNG/ClientsSmall.png", wx.BITMAP_TYPE_ANY)
        self.BitMapConfiguracoes = wx.Bitmap("PNG/ClientsSmall.png", wx.BITMAP_TYPE_ANY)
        self.BitMapSair = wx.Bitmap("PNG/ClientsSmall.png", wx.BITMAP_TYPE_ANY)

        self.BotaoClients = wx.BitmapButton(self.Tela.Painel, id = wx.ID_ANY, bitmap=self.BitMapClientes)
        self.BotaoFornecedores = wx.BitmapButton(self.Tela.Painel, id = wx.ID_ANY, bitmap=self.BitMapClientes)
        self.BotaoOSRelatorios = wx.BitmapButton(self.Tela.Painel, id = wx.ID_ANY, bitmap=self.BitMapClientes)
        self.BotaoFinanceiro = wx.BitmapButton(self.Tela.Painel, id = wx.ID_ANY, bitmap=self.BitMapClientes)
        self.BotaoOrcarmeto = wx.BitmapButton(self.Tela.Painel, id = wx.ID_ANY, bitmap=self.BitMapClientes)
        self.BotaoConfiguracoes = wx.BitmapButton(self.Tela.Painel, id = wx.ID_ANY, bitmap=self.BitMapClientes)
        self.BotaoSair = wx.Button = wx.BitmapButton(self.Tela.Painel, id = wx.ID_ANY, bitmap=self.BitMapClientes)

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

    def AoSair(self, e):
        self.Tela.Close()

class TelaConfiguracao:
    def __init__(self):
        self.Tela = Tela(None, wx.DEFAULT_FRAME_STYLE,"Sistema", "", 550, 500)

        self.Tela.Centre()
        self.Tela.Show()

class TelaControleFinanceiro:
    def __init__(self):
        self.Tela = Tela(None, wx.DEFAULT_FRAME_STYLE,"Sistema", "", 550, 500)

        self.Tela.Centre()
        self.Tela.Show()

class TelaOrdemServicos:
    def __init__(self):
        self.Tela = Tela(None, wx.DEFAULT_FRAME_STYLE,"Sistema", "", 550, 500)

        self.Tela.Centre()
        self.Tela.Show()

class TelaRelatorios:
    def __init__(self):
        self.Tela = Tela(None, wx.DEFAULT_FRAME_STYLE,"Sistema", "", 550, 500)

        self.Tela.Centre()
        self.Tela.Show()

class TelaFornecedores:
    def __init__(self):
        self.Tela = Tela(None, wx.DEFAULT_FRAME_STYLE,"Sistema", "", 550, 500)

        self.Tela.Centre()
        self.Tela.Show()

class TelaClientes:
    def __init__(self):
        self.Tela = Tela(None, wx.DEFAULT_FRAME_STYLE,"Sistema", "", 550, 500)

        self.Tela.Centre()
        self.Tela.Show()

class View:
    def __init__(self):
        self.TelaMenu = TelaMenu()
        #self.TelaLogin = TelaLogin()
        #self.TelaAutorizacao = TelaAutorizacao()

class Controller:
    def __init__(self, app):
        self.view = View()
        #self.model = Model()

if __name__ == "__main__":
    app = wx.App()
    controller = Controller(app)
    app.MainLoop()

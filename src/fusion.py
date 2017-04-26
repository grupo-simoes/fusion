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


class TelaAutorizacao:
    def __init__(self):
        self.Tela = Tela(None, wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER,"Autorizacao", "", 320, 140)

        self.InitUI()
        self.Tela.Centre()
        self.Tela.Show()

    def InitUI(self):
        self.Rotulo = wx.StaticText( self.Tela.Painel, label="Autorizacao")

        self.CaixaTexto = wx.TextCtrl(self.Tela.Painel)

        self.BotaoOk =  wx.Button(self.Tela.Painel, label='Ok')
        self.BotaoCancelar =  wx.Button(self.Tela.Painel, label='Cancelar')

        self.Tela.Bind(wx.EVT_BUTTON, self.AoClickBotaoOk, self.BotaoOk)
        self.Tela.Bind(wx.EVT_BUTTON, self.AoClickBotaoCancelar, self.BotaoCancelar))

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

class TelaFundo:
    def __init__(self):
        self.Tela = Tela(None, wx.DEFAULT_FRAME_STYLE,"Sistema", "", 550, 500)

        self.Tela.Centre()
        self.Tela.Show()
        self.Tela.Maximize(True)




class View:
    def __init__(self):
        self.TelaFundo = TelaFundo()
        self.TelaAutorizacao = TelaAutorizacao()


class Controller:
    def __init__(self, app):
        self.view = View()
        self.model = Model()


if __name__ == "__main__":
    app = wx.App()
    controller = Controller(app)
    app.MainLoop()

# Python app
class CAC {
  WebsocketAsteriskApi _asteriskApi;
  ControllerApi _controllerApi;

  List[] _callerData;

  construct(WebsocketAsteriskApi, ControllerApi, Database, WebSocketInterno) {
    this->_asteriskApi = WebsocketAsteriskApi;
    this->_controllerApi = ControllerApi;
    this->_database = Database;
  }

  threadWebSocket() {
    while (_asteriskApi.listen() == true) {
      _callerData = _asteriskApi.getData();
    
      if (_callerData.isFullRegistersIn(300)) {
        _asteriskApi.close();
      }
    }
  }

  threadControllerApi() {
    while(_callerData.registers >= 1 ) {
      metrics = _controllerApi.getMetrics();

      WebSocketInterno.send(metrics);

      sleep(1000); // 10 segundos;
    }
  }

  initApp() {
    initThreadWebSocketAsteriskApi();
    initThreadControllerAPi();
  }
}

WebSocketInterno();
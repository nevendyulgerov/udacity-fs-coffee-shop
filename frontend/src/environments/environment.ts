export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:8000', // the running FLASK api server url
  auth0: {
    url: 'neatsu', // the auth0 domain prefix
    audience: 'coffee-shop', // the audience set for the auth0 app
    clientId: 'IEn9rCg6HxdcPcV3po79RevldEFtbjan', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:4200', // the base url of the running ionic application.
  }
};

/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:8000', // the running FLASK api server url
  auth0: {
    url: 'neatsu.auth0.com', // the auth0 domain prefix
    audience: 'image', // the audience set for the auth0 app
    clientId: '7DcSDe5KHGbofMl4N6j9I3V6me4ac3Eg', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8080/login-results' // http://localhost:8100', // the base url of the running ionic application.
  }
};

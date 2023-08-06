this.workbox=this.workbox||{};this.workbox.routing=(function(exports,assert_mjs,logger_mjs,cacheNames_mjs,WorkboxError_mjs,getFriendlyURL_mjs){'use strict';try{self['workbox:routing:4.3.1']&&_();}catch(e){}
const defaultMethod='GET';const validMethods=['DELETE','GET','HEAD','PATCH','POST','PUT'];const normalizeHandler=handler=>{if(handler&&typeof handler==='object'){{assert_mjs.assert.hasMethod(handler,'handle',{moduleName:'workbox-routing',className:'Route',funcName:'constructor',paramName:'handler'});}
return handler;}else{{assert_mjs.assert.isType(handler,'function',{moduleName:'workbox-routing',className:'Route',funcName:'constructor',paramName:'handler'});}
return{handle:handler};}};class Route{constructor(match,handler,method){{assert_mjs.assert.isType(match,'function',{moduleName:'workbox-routing',className:'Route',funcName:'constructor',paramName:'match'});if(method){assert_mjs.assert.isOneOf(method,validMethods,{paramName:'method'});}}
this.handler=normalizeHandler(handler);this.match=match;this.method=method||defaultMethod;}}
class NavigationRoute extends Route{constructor(handler,{whitelist=[/./],blacklist=[]}={}){{assert_mjs.assert.isArrayOfClass(whitelist,RegExp,{moduleName:'workbox-routing',className:'NavigationRoute',funcName:'constructor',paramName:'options.whitelist'});assert_mjs.assert.isArrayOfClass(blacklist,RegExp,{moduleName:'workbox-routing',className:'NavigationRoute',funcName:'constructor',paramName:'options.blacklist'});}
super(options=>this._match(options),handler);this._whitelist=whitelist;this._blacklist=blacklist;}
_match({url,request}){if(request.mode!=='navigate'){return false;}
const pathnameAndSearch=url.pathname+url.search;for(const regExp of this._blacklist){if(regExp.test(pathnameAndSearch)){{logger_mjs.logger.log(`The navigation route is not being used, since the `+`URL matches this blacklist pattern: ${regExp}`);}
return false;}}
if(this._whitelist.some(regExp=>regExp.test(pathnameAndSearch))){{logger_mjs.logger.debug(`The navigation route is being used.`);}
return true;}
{logger_mjs.logger.log(`The navigation route is not being used, since the URL `+`being navigated to doesn't match the whitelist.`);}
return false;}}
class RegExpRoute extends Route{constructor(regExp,handler,method){{assert_mjs.assert.isInstance(regExp,RegExp,{moduleName:'workbox-routing',className:'RegExpRoute',funcName:'constructor',paramName:'pattern'});}
const match=({url})=>{const result=regExp.exec(url.href);if(!result){return null;}
if(url.origin!==location.origin&&result.index!==0){{logger_mjs.logger.debug(`The regular expression '${regExp}' only partially matched `+`against the cross-origin URL '${url}'. RegExpRoute's will only `+`handle cross-origin requests if they match the entire URL.`);}
return null;}
return result.slice(1);};super(match,handler,method);}}
class Router{constructor(){this._routes=new Map();}
get routes(){return this._routes;}
addFetchListener(){self.addEventListener('fetch',event=>{const{request}=event;const responsePromise=this.handleRequest({request,event});if(responsePromise){event.respondWith(responsePromise);}});}
addCacheListener(){self.addEventListener('message',async event=>{if(event.data&&event.data.type==='CACHE_URLS'){const{payload}=event.data;{logger_mjs.logger.debug(`Caching URLs from the window`,payload.urlsToCache);}
const requestPromises=Promise.all(payload.urlsToCache.map(entry=>{if(typeof entry==='string'){entry=[entry];}
const request=new Request(...entry);return this.handleRequest({request});}));event.waitUntil(requestPromises);if(event.ports&&event.ports[0]){await requestPromises;event.ports[0].postMessage(true);}}});}
handleRequest({request,event}){{assert_mjs.assert.isInstance(request,Request,{moduleName:'workbox-routing',className:'Router',funcName:'handleRequest',paramName:'options.request'});}
const url=new URL(request.url,location);if(!url.protocol.startsWith('http')){{logger_mjs.logger.debug(`Workbox Router only supports URLs that start with 'http'.`);}
return;}
let{params,route}=this.findMatchingRoute({url,request,event});let handler=route&&route.handler;let debugMessages=[];{if(handler){debugMessages.push([`Found a route to handle this request:`,route]);if(params){debugMessages.push([`Passing the following params to the route's handler:`,params]);}}}
if(!handler&&this._defaultHandler){{debugMessages.push(`Failed to find a matching route. Falling `+`back to the default handler.`);route='[Default Handler]';}
handler=this._defaultHandler;}
if(!handler){{logger_mjs.logger.debug(`No route found for: ${getFriendlyURL_mjs.getFriendlyURL(url)}`);}
return;}
{logger_mjs.logger.groupCollapsed(`Router is responding to: ${getFriendlyURL_mjs.getFriendlyURL(url)}`);debugMessages.forEach(msg=>{if(Array.isArray(msg)){logger_mjs.logger.log(...msg);}else{logger_mjs.logger.log(msg);}});logger_mjs.logger.groupCollapsed(`View request details here.`);logger_mjs.logger.log(request);logger_mjs.logger.groupEnd();logger_mjs.logger.groupEnd();}
let responsePromise;try{responsePromise=handler.handle({url,request,event,params});}catch(err){responsePromise=Promise.reject(err);}
if(responsePromise&&this._catchHandler){responsePromise=responsePromise.catch(err=>{{logger_mjs.logger.groupCollapsed(`Error thrown when responding to: `+` ${getFriendlyURL_mjs.getFriendlyURL(url)}. Falling back to Catch Handler.`);logger_mjs.logger.error(`Error thrown by:`,route);logger_mjs.logger.error(err);logger_mjs.logger.groupEnd();}
return this._catchHandler.handle({url,event,err});});}
return responsePromise;}
findMatchingRoute({url,request,event}){{assert_mjs.assert.isInstance(url,URL,{moduleName:'workbox-routing',className:'Router',funcName:'findMatchingRoute',paramName:'options.url'});assert_mjs.assert.isInstance(request,Request,{moduleName:'workbox-routing',className:'Router',funcName:'findMatchingRoute',paramName:'options.request'});}
const routes=this._routes.get(request.method)||[];for(const route of routes){let params;let matchResult=route.match({url,request,event});if(matchResult){if(Array.isArray(matchResult)&&matchResult.length>0){params=matchResult;}else if(matchResult.constructor===Object&&Object.keys(matchResult).length>0){params=matchResult;}
return{route,params};}}
return{};}
setDefaultHandler(handler){this._defaultHandler=normalizeHandler(handler);}
setCatchHandler(handler){this._catchHandler=normalizeHandler(handler);}
registerRoute(route){{assert_mjs.assert.isType(route,'object',{moduleName:'workbox-routing',className:'Router',funcName:'registerRoute',paramName:'route'});assert_mjs.assert.hasMethod(route,'match',{moduleName:'workbox-routing',className:'Router',funcName:'registerRoute',paramName:'route'});assert_mjs.assert.isType(route.handler,'object',{moduleName:'workbox-routing',className:'Router',funcName:'registerRoute',paramName:'route'});assert_mjs.assert.hasMethod(route.handler,'handle',{moduleName:'workbox-routing',className:'Router',funcName:'registerRoute',paramName:'route.handler'});assert_mjs.assert.isType(route.method,'string',{moduleName:'workbox-routing',className:'Router',funcName:'registerRoute',paramName:'route.method'});}
if(!this._routes.has(route.method)){this._routes.set(route.method,[]);}
this._routes.get(route.method).push(route);}
unregisterRoute(route){if(!this._routes.has(route.method)){throw new WorkboxError_mjs.WorkboxError('unregister-route-but-not-found-with-method',{method:route.method});}
const routeIndex=this._routes.get(route.method).indexOf(route);if(routeIndex>-1){this._routes.get(route.method).splice(routeIndex,1);}else{throw new WorkboxError_mjs.WorkboxError('unregister-route-route-not-registered');}}}
let defaultRouter;const getOrCreateDefaultRouter=()=>{if(!defaultRouter){defaultRouter=new Router();defaultRouter.addFetchListener();defaultRouter.addCacheListener();}
return defaultRouter;};const registerNavigationRoute=(cachedAssetUrl,options={})=>{{assert_mjs.assert.isType(cachedAssetUrl,'string',{moduleName:'workbox-routing',funcName:'registerNavigationRoute',paramName:'cachedAssetUrl'});}
const cacheName=cacheNames_mjs.cacheNames.getPrecacheName(options.cacheName);const handler=async()=>{try{const response=await caches.match(cachedAssetUrl,{cacheName});if(response){return response;}
throw new Error(`The cache ${cacheName} did not have an entry for `+`${cachedAssetUrl}.`);}catch(error){{logger_mjs.logger.debug(`Unable to respond to navigation request with `+`cached response. Falling back to network.`,error);}
return fetch(cachedAssetUrl);}};const route=new NavigationRoute(handler,{whitelist:options.whitelist,blacklist:options.blacklist});const defaultRouter=getOrCreateDefaultRouter();defaultRouter.registerRoute(route);return route;};const registerRoute=(capture,handler,method='GET')=>{let route;if(typeof capture==='string'){const captureUrl=new URL(capture,location);{if(!(capture.startsWith('/')||capture.startsWith('http'))){throw new WorkboxError_mjs.WorkboxError('invalid-string',{moduleName:'workbox-routing',funcName:'registerRoute',paramName:'capture'});}
const valueToCheck=capture.startsWith('http')?captureUrl.pathname:capture;const wildcards='[*:?+]';if(valueToCheck.match(new RegExp(`${wildcards}`))){logger_mjs.logger.debug(`The '$capture' parameter contains an Express-style wildcard `+`character (${wildcards}). Strings are now always interpreted as `+`exact matches; use a RegExp for partial or wildcard matches.`);}}
const matchCallback=({url})=>{{if(url.pathname===captureUrl.pathname&&url.origin!==captureUrl.origin){logger_mjs.logger.debug(`${capture} only partially matches the cross-origin URL `+`${url}. This route will only handle cross-origin requests `+`if they match the entire URL.`);}}
return url.href===captureUrl.href;};route=new Route(matchCallback,handler,method);}else if(capture instanceof RegExp){route=new RegExpRoute(capture,handler,method);}else if(typeof capture==='function'){route=new Route(capture,handler,method);}else if(capture instanceof Route){route=capture;}else{throw new WorkboxError_mjs.WorkboxError('unsupported-route-type',{moduleName:'workbox-routing',funcName:'registerRoute',paramName:'capture'});}
const defaultRouter=getOrCreateDefaultRouter();defaultRouter.registerRoute(route);return route;};const setCatchHandler=handler=>{const defaultRouter=getOrCreateDefaultRouter();defaultRouter.setCatchHandler(handler);};const setDefaultHandler=handler=>{const defaultRouter=getOrCreateDefaultRouter();defaultRouter.setDefaultHandler(handler);};{assert_mjs.assert.isSWEnv('workbox-routing');}
exports.NavigationRoute=NavigationRoute;exports.RegExpRoute=RegExpRoute;exports.registerNavigationRoute=registerNavigationRoute;exports.registerRoute=registerRoute;exports.Route=Route;exports.Router=Router;exports.setCatchHandler=setCatchHandler;exports.setDefaultHandler=setDefaultHandler;return exports;}({},workbox.core._private,workbox.core._private,workbox.core._private,workbox.core._private,workbox.core._private));
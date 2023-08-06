this.workbox=this.workbox||{};this.workbox.strategies=(function(exports,logger_mjs,assert_mjs,cacheNames_mjs,cacheWrapper_mjs,fetchWrapper_mjs,getFriendlyURL_mjs,WorkboxError_mjs){'use strict';try{self['workbox:strategies:4.3.1']&&_();}catch(e){}
const getFriendlyURL=url=>{const urlObj=new URL(url,location);if(urlObj.origin===location.origin){return urlObj.pathname;}
return urlObj.href;};const messages={strategyStart:(strategyName,request)=>`Using ${strategyName} to `+`respond to '${getFriendlyURL(request.url)}'`,printFinalResponse:response=>{if(response){logger_mjs.logger.groupCollapsed(`View the final response here.`);logger_mjs.logger.log(response);logger_mjs.logger.groupEnd();}}};class CacheFirst{constructor(options={}){this._cacheName=cacheNames_mjs.cacheNames.getRuntimeName(options.cacheName);this._plugins=options.plugins||[];this._fetchOptions=options.fetchOptions||null;this._matchOptions=options.matchOptions||null;}
async handle({event,request}){return this.makeRequest({event,request:request||event.request});}
async makeRequest({event,request}){const logs=[];if(typeof request==='string'){request=new Request(request);}
{assert_mjs.assert.isInstance(request,Request,{moduleName:'workbox-strategies',className:'CacheFirst',funcName:'makeRequest',paramName:'request'});}
let response=await cacheWrapper_mjs.cacheWrapper.match({cacheName:this._cacheName,request,event,matchOptions:this._matchOptions,plugins:this._plugins});let error;if(!response){{logs.push(`No response found in the '${this._cacheName}' cache. `+`Will respond with a network request.`);}
try{response=await this._getFromNetwork(request,event);}catch(err){error=err;}
{if(response){logs.push(`Got response from network.`);}else{logs.push(`Unable to get a response from the network.`);}}}else{{logs.push(`Found a cached response in the '${this._cacheName}' cache.`);}}
{logger_mjs.logger.groupCollapsed(messages.strategyStart('CacheFirst',request));for(let log of logs){logger_mjs.logger.log(log);}
messages.printFinalResponse(response);logger_mjs.logger.groupEnd();}
if(!response){throw new WorkboxError_mjs.WorkboxError('no-response',{url:request.url,error});}
return response;}
async _getFromNetwork(request,event){const response=await fetchWrapper_mjs.fetchWrapper.fetch({request,event,fetchOptions:this._fetchOptions,plugins:this._plugins});const responseClone=response.clone();const cachePutPromise=cacheWrapper_mjs.cacheWrapper.put({cacheName:this._cacheName,request,response:responseClone,event,plugins:this._plugins});if(event){try{event.waitUntil(cachePutPromise);}catch(error){{logger_mjs.logger.warn(`Unable to ensure service worker stays alive when `+`updating cache for '${getFriendlyURL_mjs.getFriendlyURL(request.url)}'.`);}}}
return response;}}
class CacheOnly{constructor(options={}){this._cacheName=cacheNames_mjs.cacheNames.getRuntimeName(options.cacheName);this._plugins=options.plugins||[];this._matchOptions=options.matchOptions||null;}
async handle({event,request}){return this.makeRequest({event,request:request||event.request});}
async makeRequest({event,request}){if(typeof request==='string'){request=new Request(request);}
{assert_mjs.assert.isInstance(request,Request,{moduleName:'workbox-strategies',className:'CacheOnly',funcName:'makeRequest',paramName:'request'});}
const response=await cacheWrapper_mjs.cacheWrapper.match({cacheName:this._cacheName,request,event,matchOptions:this._matchOptions,plugins:this._plugins});{logger_mjs.logger.groupCollapsed(messages.strategyStart('CacheOnly',request));if(response){logger_mjs.logger.log(`Found a cached response in the '${this._cacheName}'`+` cache.`);messages.printFinalResponse(response);}else{logger_mjs.logger.log(`No response found in the '${this._cacheName}' cache.`);}
logger_mjs.logger.groupEnd();}
if(!response){throw new WorkboxError_mjs.WorkboxError('no-response',{url:request.url});}
return response;}}
const cacheOkAndOpaquePlugin={cacheWillUpdate:({response})=>{if(response.status===200||response.status===0){return response;}
return null;}};class NetworkFirst{constructor(options={}){this._cacheName=cacheNames_mjs.cacheNames.getRuntimeName(options.cacheName);if(options.plugins){let isUsingCacheWillUpdate=options.plugins.some(plugin=>!!plugin.cacheWillUpdate);this._plugins=isUsingCacheWillUpdate?options.plugins:[cacheOkAndOpaquePlugin,...options.plugins];}else{this._plugins=[cacheOkAndOpaquePlugin];}
this._networkTimeoutSeconds=options.networkTimeoutSeconds;{if(this._networkTimeoutSeconds){assert_mjs.assert.isType(this._networkTimeoutSeconds,'number',{moduleName:'workbox-strategies',className:'NetworkFirst',funcName:'constructor',paramName:'networkTimeoutSeconds'});}}
this._fetchOptions=options.fetchOptions||null;this._matchOptions=options.matchOptions||null;}
async handle({event,request}){return this.makeRequest({event,request:request||event.request});}
async makeRequest({event,request}){const logs=[];if(typeof request==='string'){request=new Request(request);}
{assert_mjs.assert.isInstance(request,Request,{moduleName:'workbox-strategies',className:'NetworkFirst',funcName:'handle',paramName:'makeRequest'});}
const promises=[];let timeoutId;if(this._networkTimeoutSeconds){const{id,promise}=this._getTimeoutPromise({request,event,logs});timeoutId=id;promises.push(promise);}
const networkPromise=this._getNetworkPromise({timeoutId,request,event,logs});promises.push(networkPromise);let response=await Promise.race(promises);if(!response){response=await networkPromise;}
{logger_mjs.logger.groupCollapsed(messages.strategyStart('NetworkFirst',request));for(let log of logs){logger_mjs.logger.log(log);}
messages.printFinalResponse(response);logger_mjs.logger.groupEnd();}
if(!response){throw new WorkboxError_mjs.WorkboxError('no-response',{url:request.url});}
return response;}
_getTimeoutPromise({request,logs,event}){let timeoutId;const timeoutPromise=new Promise(resolve=>{const onNetworkTimeout=async()=>{{logs.push(`Timing out the network response at `+`${this._networkTimeoutSeconds} seconds.`);}
resolve((await this._respondFromCache({request,event})));};timeoutId=setTimeout(onNetworkTimeout,this._networkTimeoutSeconds*1000);});return{promise:timeoutPromise,id:timeoutId};}
async _getNetworkPromise({timeoutId,request,logs,event}){let error;let response;try{response=await fetchWrapper_mjs.fetchWrapper.fetch({request,event,fetchOptions:this._fetchOptions,plugins:this._plugins});}catch(err){error=err;}
if(timeoutId){clearTimeout(timeoutId);}
{if(response){logs.push(`Got response from network.`);}else{logs.push(`Unable to get a response from the network. Will respond `+`with a cached response.`);}}
if(error||!response){response=await this._respondFromCache({request,event});{if(response){logs.push(`Found a cached response in the '${this._cacheName}'`+` cache.`);}else{logs.push(`No response found in the '${this._cacheName}' cache.`);}}}else{const responseClone=response.clone();const cachePut=cacheWrapper_mjs.cacheWrapper.put({cacheName:this._cacheName,request,response:responseClone,event,plugins:this._plugins});if(event){try{event.waitUntil(cachePut);}catch(err){{logger_mjs.logger.warn(`Unable to ensure service worker stays alive when `+`updating cache for '${getFriendlyURL_mjs.getFriendlyURL(request.url)}'.`);}}}}
return response;}
_respondFromCache({event,request}){return cacheWrapper_mjs.cacheWrapper.match({cacheName:this._cacheName,request,event,matchOptions:this._matchOptions,plugins:this._plugins});}}
class NetworkOnly{constructor(options={}){this._cacheName=cacheNames_mjs.cacheNames.getRuntimeName(options.cacheName);this._plugins=options.plugins||[];this._fetchOptions=options.fetchOptions||null;}
async handle({event,request}){return this.makeRequest({event,request:request||event.request});}
async makeRequest({event,request}){if(typeof request==='string'){request=new Request(request);}
{assert_mjs.assert.isInstance(request,Request,{moduleName:'workbox-strategies',className:'NetworkOnly',funcName:'handle',paramName:'request'});}
let error;let response;try{response=await fetchWrapper_mjs.fetchWrapper.fetch({request,event,fetchOptions:this._fetchOptions,plugins:this._plugins});}catch(err){error=err;}
{logger_mjs.logger.groupCollapsed(messages.strategyStart('NetworkOnly',request));if(response){logger_mjs.logger.log(`Got response from network.`);}else{logger_mjs.logger.log(`Unable to get a response from the network.`);}
messages.printFinalResponse(response);logger_mjs.logger.groupEnd();}
if(!response){throw new WorkboxError_mjs.WorkboxError('no-response',{url:request.url,error});}
return response;}}
class StaleWhileRevalidate{constructor(options={}){this._cacheName=cacheNames_mjs.cacheNames.getRuntimeName(options.cacheName);this._plugins=options.plugins||[];if(options.plugins){let isUsingCacheWillUpdate=options.plugins.some(plugin=>!!plugin.cacheWillUpdate);this._plugins=isUsingCacheWillUpdate?options.plugins:[cacheOkAndOpaquePlugin,...options.plugins];}else{this._plugins=[cacheOkAndOpaquePlugin];}
this._fetchOptions=options.fetchOptions||null;this._matchOptions=options.matchOptions||null;}
async handle({event,request}){return this.makeRequest({event,request:request||event.request});}
async makeRequest({event,request}){const logs=[];if(typeof request==='string'){request=new Request(request);}
{assert_mjs.assert.isInstance(request,Request,{moduleName:'workbox-strategies',className:'StaleWhileRevalidate',funcName:'handle',paramName:'request'});}
const fetchAndCachePromise=this._getFromNetwork({request,event});let response=await cacheWrapper_mjs.cacheWrapper.match({cacheName:this._cacheName,request,event,matchOptions:this._matchOptions,plugins:this._plugins});let error;if(response){{logs.push(`Found a cached response in the '${this._cacheName}'`+` cache. Will update with the network response in the background.`);}
if(event){try{event.waitUntil(fetchAndCachePromise);}catch(error){{logger_mjs.logger.warn(`Unable to ensure service worker stays alive when `+`updating cache for '${getFriendlyURL_mjs.getFriendlyURL(request.url)}'.`);}}}}else{{logs.push(`No response found in the '${this._cacheName}' cache. `+`Will wait for the network response.`);}
try{response=await fetchAndCachePromise;}catch(err){error=err;}}
{logger_mjs.logger.groupCollapsed(messages.strategyStart('StaleWhileRevalidate',request));for(let log of logs){logger_mjs.logger.log(log);}
messages.printFinalResponse(response);logger_mjs.logger.groupEnd();}
if(!response){throw new WorkboxError_mjs.WorkboxError('no-response',{url:request.url,error});}
return response;}
async _getFromNetwork({request,event}){const response=await fetchWrapper_mjs.fetchWrapper.fetch({request,event,fetchOptions:this._fetchOptions,plugins:this._plugins});const cachePutPromise=cacheWrapper_mjs.cacheWrapper.put({cacheName:this._cacheName,request,response:response.clone(),event,plugins:this._plugins});if(event){try{event.waitUntil(cachePutPromise);}catch(error){{logger_mjs.logger.warn(`Unable to ensure service worker stays alive when `+`updating cache for '${getFriendlyURL_mjs.getFriendlyURL(request.url)}'.`);}}}
return response;}}
const mapping={cacheFirst:CacheFirst,cacheOnly:CacheOnly,networkFirst:NetworkFirst,networkOnly:NetworkOnly,staleWhileRevalidate:StaleWhileRevalidate};const deprecate=strategy=>{const StrategyCtr=mapping[strategy];return options=>{{const strategyCtrName=strategy[0].toUpperCase()+strategy.slice(1);logger_mjs.logger.warn(`The 'workbox.strategies.${strategy}()' function has been `+`deprecated and will be removed in a future version of Workbox.\n`+`Please use 'new workbox.strategies.${strategyCtrName}()' instead.`);}
return new StrategyCtr(options);};};const cacheFirst=deprecate('cacheFirst');const cacheOnly=deprecate('cacheOnly');const networkFirst=deprecate('networkFirst');const networkOnly=deprecate('networkOnly');const staleWhileRevalidate=deprecate('staleWhileRevalidate');exports.CacheFirst=CacheFirst;exports.CacheOnly=CacheOnly;exports.NetworkFirst=NetworkFirst;exports.NetworkOnly=NetworkOnly;exports.StaleWhileRevalidate=StaleWhileRevalidate;exports.cacheFirst=cacheFirst;exports.cacheOnly=cacheOnly;exports.networkFirst=networkFirst;exports.networkOnly=networkOnly;exports.staleWhileRevalidate=staleWhileRevalidate;return exports;}({},workbox.core._private,workbox.core._private,workbox.core._private,workbox.core._private,workbox.core._private,workbox.core._private,workbox.core._private));
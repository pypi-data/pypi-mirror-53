function testdone(name,callback){if(callback===undefined){callback=name;name="render";}
let time=50;let promise_callbacks={resolve:undefined,reject:undefined,};let promise=new Promise((resolve,reject)=>{promise_callbacks.resolve=resolve;promise_callbacks.reject=reject;});setTimeout((name)=>{setTimeout(()=>{if(callback){callback(name);}
promise_callbacks.resolve();},time)},time,name,0);return promise;}
window.qunitTestsArray={};class TestsRunner{constructor(){this.amount=0;this.executed_tests=[];this.running=false;}
setAmount(amount){this.amount=amount;}
addTestResult(result){this.executed_tests.push(result);}
setRunning(value){this.running=value;}
numberOfRunningTest(){return this.executed_tests.length;}
amountOfRemainTests(){return this.amount-this.executed_tests.length;}
allTestsRun(){return this.amount==this.executed_tests.length;}
allTestsPassed(){return!this.executed_tests.some(test=>test.passed==false);}
getTotalRuntime(){return this.executed_tests.reduce((counter,current)=>{return counter+=current.runtime;},0);}
getFailedTests(){return this.executed_tests.filter(test=>!test.passed);}
getTestsAmountInfo(){return this.executed_tests.reduce((counter,current)=>{counter.total++;counter[current.passed?'passed':'failed']++;return counter;},{total:0,passed:0,failed:0});}
getAssertionsAmountInfo(){return this.executed_tests.reduce((counter,current)=>{['total','passed','failed'].forEach(prop=>{counter[prop]+=current.assertions[prop]});return counter;},{total:0,passed:0,failed:0});}
getTestsStatus(){if(this.running){return'RUNNING';}
if(!this.running&&this.executed_tests.length>0){return'EXECUTED';}
return'WAITING';}
getReport(){let tests=this.getTestsAmountInfo();let assertions=this.getAssertionsAmountInfo();return'Tests status: '+this.getTestsStatus()+'. \n \n'+
'Test execution runtime: '+this.getTotalRuntime()/1000+' seconds. \n \n'+
'Total tests amount: '+this.amount+'. \n \n'+
'Executed tests info: \n'+
'  - Total:  '+tests.total+'. \n'+
'  - Passed: '+tests.passed+'. \n'+
'  - Failed: '+tests.failed+'. \n \n'+
'Executed assertions info: \n'+
'  - Total:  '+assertions.total+'. \n'+
'  - Passed: '+assertions.passed+'. \n'+
'  - Failed: '+assertions.failed+'.';}
runTests(){console.log('Tests status: '+this.getTestsStatus()+'.');$("body").append('<link rel="stylesheet" href="'+hostname+window.guiStaticPath+'js/tests/phantomjs/qunit/qunit-2.2.1.css">');$("body").append('<script src="'+hostname+window.guiStaticPath+'js/tests/phantomjs/qunit/qunit-2.2.1.js"></script>');$("body").append('<div id="qunit"></div><div id="qunit-fixture"></div>');let intervalId=setInterval(()=>{if(!window.QUnit){return;}
console.log("Start of qUnit tests.");clearInterval(intervalId);QUnit.done(details=>{this.setRunning(false);console.log(this.getReport());});QUnit.testDone(details=>{let result={module_name:details.module,test_name:details.name,assertions:{total:details.total,passed:details.passed,failed:details.failed,},skipped:details.skipped,runtime:details.runtime,passed:details.total==details.passed,};this.addTestResult(result);if(!syncQUnit.nextTest()){this.showReport();testdone("ok-done",window.close);}});for(let i in window.qunitTestsArray){window.qunitTestsArray[i].test.call();}
this.setAmount(syncQUnit.testsArray.length);this.setRunning(true);syncQUnit.nextTest();console.log('Tests status: '+this.getTestsStatus()+'.');},1000);}
showReport(){$("body").html('<div id="qunit-saveReport"></div><div id="qunit">'+$("#qunit").html()+'</div>');$("body").append('<link rel="stylesheet" href="'+hostname+window.guiStaticPath+'js/tests/phantomjs/qunit/qunit-2.2.1.css">');document.getElementById("qunit-urlconfig-hidepassed").onclick=function(){let elements=Array.from(document.getElementById('qunit-tests').getElementsByClassName('pass'));elements.forEach(el=>{el.hidden=this.checked});}}}
var _guiTestsRunner=new TestsRunner();syncQUnit={};syncQUnit.testsArray=[];syncQUnit.addTest=function(name,test){syncQUnit.testsArray.push({name:name,test:test})};syncQUnit.nextTest=function(){if(!syncQUnit.testsArray.length){return false;}
let test=syncQUnit.testsArray.shift();guiPopUp.warning("Test "+test.name+", "+syncQUnit.testsArray.length+" tests remain");QUnit.test(test.name,test.test);return true;};window.qunitTestsArray['trim']={test:function(){syncQUnit.addTest('trim',function(assert){let done=assert.async();assert.equal(trim(''),'','Empty string');assert.ok(trim('   ')==='','String with spaces symbols');assert.equal(trim(),'','No argument was passed');assert.equal(trim(' x'),'x','Spaces at the beginning of string');assert.equal(trim('x '),'x','Spaces at the end of string');assert.equal(trim(' x '),'x','Spaces at the beginning and at the end of string');assert.equal(trim('    x  '),'x','Tabs');assert.equal(trim('    x   y  '),'x   y','Tabs and strings inside string');testdone(done);});}};
// variable injection
var awsRegion = document.getElementById('awsRegion').title;
var kinesisStreamName = document.getElementById('kinesisStreamName').title;
var cognitoPoolId = document.getElementById('cognitoPoolId').title;
var deliveryId = document.getElementById('deliveryId').title;
var versions = document.getElementById('versions').title;
var language = document.getElementById('language').title;

// Parse versions and get version
arr = versions.split(',')
arr.forEach(function (v) {
    if (v.indexOf('fr')){
        version = v.split(':')[1]
    }
})

// Generate uuid func
function generateUuid() {
    // https://github.com/GoogleChrome/chrome-platform-analytics/blob/master/src/internal/identifier.js
    // const FORMAT: string = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx";
    let chars = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".split("");
    for (let i = 0, len = chars.length; i < len; i++) {
        switch (chars[i]) {
            case "x":
                chars[i] = Math.floor(Math.random() * 16).toString(16);
                break;
            case "y":
                chars[i] = (Math.floor(Math.random() * 4) + 8).toString(16);
                break;
        }
    }
    return chars.join("");
}


// Configure Credentials to use Cognito
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: cognitoPoolId
});
AWS.config.region = awsRegion;
AWS.config.credentials.get(function (err) {
    if (err) {
        // alert('Error retrieving credentials.');
        console.error(err);
        return;
    }
    // create Amazon Kinesis service object
    var kinesis = new AWS.Kinesis({
        apiVersion: '2013-12-02'
    });

    // create user Id
    var userId
    var isRegisteredered
    // check whether user use HTML5
    if (window.localStorage) {
        // generate uuid if not data in localstorage
        userId = localStorage.getItem('userId');
        isRegistered = 'false';
        if (userId == null) {
            userId = generateUuid();
            localStorage.setItem('userId', userId);
            isRegistered = 'true';
        }
    } else {
        userId = 'guestUser'
    }


    // create Amazon Kinesis service object
    var kinesis = new AWS.Kinesis({
        apiVersion: '2013-12-02'
    });
    var recordData = [];
    var record = {
        Data: JSON.stringify({
            page_path: window.location.pathname,
            delivery_id: deliveryId,
            user_id: userId,
            is_regitered: isRegistered,
            version: version,
            language: language
        }),
        PartitionKey: 'partition-' + userId
    };
    recordData.push(record);

    kinesis.putRecords({
                Records: recordData,
                StreamName: kinesisStreamName
            }, function(err, data) {
                if (err) {
                    console.error(err);
                }
        });
    
});
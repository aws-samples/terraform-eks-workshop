// variable injection
var awsRegion = document.getElementById('awsRegion').title;
var kinesisStreamName = document.getElementById('kinesisStreamName').title;
var cognitoPoolId = document.getElementById('cognitoPoolId').title;
var eventId = document.getElementById('eventId').title;

// deault:10sec
var interval = 10;

// Parse versions and get version
arr = versions.split(',')
arr.forEach(function (v) {
    if (v.indexOf(language)) {
        version = v.split(':')[1]
    }
})

// Send log to Kinesis
var sendLog = function () {
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
        // check whether user use HTML5
        if (window.localStorage) {
            // generate userId if not data in localstorage
            userId = localStorage.getItem('userId');
            isRegistered = 'false';
            if (userId == null) {
                userId = AWS.config.credentials.identityId;
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
        }, function (err, data) {
            if (err) {
                console.error(err);
            }
        });

    });
};

var is_focus = false;
// Call Send Log Func by every 10 sec when the Tab is focused 
window.onfocus = function () {
    is_focus = true;
}
window.onblur = function () {
    is_focus = false;
}

var check_interval = setInterval(function () {
    if (is_focus) {
        sendLog();
    }
}, interval * 1000);
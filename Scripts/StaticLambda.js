exports.handler = async (event) => {
    const exec = require('child_process').exec;
    const command = event.body.command;
    return new Promise((resolve, reject) => {
        exec(command, (error, stdout, stderr) => {
            if (error) {
                reject(error);
            } else {
                resolve(stdout);
            }
        });
    });
};

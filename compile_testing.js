var fs = require('fs');
var dir = './testing-folder';

if (!fs.existsSync(dir)){
    fs.mkdirSync(dir);
}

var package_files = [];
var command_list = [];

// For each folder in ./examples
var examples = fs.readdirSync('./examples');
for (var i = 0; i < examples.length; i++) {
    var example = examples[i];
    var examplePath = './examples/' + example;
    if (fs.lstatSync(examplePath).isDirectory()) {
        var files = fs.readdirSync(examplePath);
        for (var j = 0; j < files.length; j++) {
            var file = files[j];

            // If file is a .js file, copy it to ./testing-folder
            if (file.endsWith('.js')) {
                let dup_name = example + '_' + file;
                var filePath = examplePath + '/' + file;
                fs.copyFile(filePath, './testing-folder/' + dup_name, (err) => {
                    if (err) throw err;
                    console.log('Copied to ./testing-folder/' + dup_name);
                });
            }

            // If file is a package.json file, copy it to ./testing-folder
            if (file.endsWith('package.json')) {
                let dup_name = example + '_' + file;
                var filePath = examplePath + '/' + file;
                fs.copyFile(filePath, './testing-folder/' + dup_name, (err) => {
                    if (err) throw err;
                    console.log('Copied to ./testing-folder/' + dup_name);
                });
                package_files.push(dup_name);
            }

            // If file is a README.md, add the dataset download command to a list of commands
            if (file.endsWith('README.md')) {
                var filePath = examplePath + '/' + file;
                var data = fs.readFileSync(filePath, 'utf8');
                var lines = data.split('\n');
                let start = false;
                for (var k = 0; k < lines.length; k++) {
                    if (lines[k].startsWith('```bash')) {
                        start = true;
                        continue;
                    }
                    else if (lines[k].startsWith('```')) {
                        start = false;
                        continue;
                    }
                    if (start) {
                        command_list.push(lines[k]);
                    }
                }
            }
        }
    }

}

fs.copyFile("package.json", './testing-folder/' + "old-package.json", (err) => {
    if (err) throw err;
    console.log('package.json was copied to ./testing-folder/old-package.json');
});
package_files.push("old-package.json");

// Create package merge command
var command = "package-json-merge " + package_files.join(' ') + " > package.json";
fs.writeFile('./testing-folder/merge-package.sh', command, function (err) {});

// Create dataset download command
fs.writeFile('./testing-folder/commands.sh', command_list.join('\n'), function (err) {});
const express = require('express'); // express 모듈 가져오기
const cors = require('cors'); // cors 모듈 가져오기
const PORT = 8000;
const path = require('path'); // path 모듈을 불러옵니다.
const bodyParser = require('body-parser');
const spawn = require('child_process').spawn;

const app = express(); // express 모듈을 사용하기 위해 app 변수에 할당한다.

app.use(bodyParser.json()); // Parse application/json content-type
app.use(cors()); //htpp, https 프로토콜을 사용하는 서버 간의 통신을 허용한다.
app.use(express.json()); // express 모듈의 json() 메소드를 사용한다.

app.get('/', (req, res) => {
  res.send('Hello Wolrd https test completed');
});

app.post('/chat', (req, res) => {
  const sendQuestion = req.body.question;
  // console.log(sendQuestion);

  const execPython = path.join(__dirname, 'aitest.py');
  const pythonPath = path.join(__dirname, 'venv', 'bin', 'python3');
  const result = spawn(pythonPath, [
    execPython,
    JSON.stringify({ question: sendQuestion }),
  ]);

  output = '';

  result.stdout.on('data', function (data) {
    output += data.toString();
  });

  result.on('close', (code) => {
    if (code === 0) {
      res.status(200).json(JSON.parse(output));
    } else {
      res.status(500).send('Something went wrong');
    }
  });
});

app.listen(PORT, () => console.log(`Server is running on ${PORT}`));

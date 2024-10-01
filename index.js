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
  res.send('Hello Wolrd test completed');
});

app.post('/weather', async (req, res) => {
  const location = req.body.location;

  // Python 스크립트와 가상 환경 경로 설정
  const execPython = path.join(__dirname, 'aitest.py');
  const pythonPath = path.join(__dirname, 'venv', 'bin', 'python3');

  // Python 스크립트를 실행
  const result = spawn(pythonPath, [execPython, JSON.stringify({ location })]);

  let output = '';

  result.stdout.on('data', (data) => {
    output += data.toString(); // Python 스크립트의 출력을 저장
  });

  result.on('close', (code) => {
    if (code === 0) {
      res.status(200).json(JSON.parse(output)); // JSON 형식으로 클라이언트에 응답
    } else {
      res.status(500).send('Something went wrong'); // 오류 처리
    }
  });
});

app.listen(PORT, () => console.log(`Server is running on ${PORT}`));

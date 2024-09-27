const express = require('express'); // express 모듈 가져오기
const cors = require('cors'); // cors 모듈 가져오기
const PORT = 8000;
const bodyParser = require('body-parser');
const spawn = require('child_process').spawn;

const app = express(); // express 모듈을 사용하기 위해 app 변수에 할당한다.

app.use(cors()); //htpp, https 프로토콜을 사용하는 서버 간의 통신을 허용한다.
app.use(express.json()); // express 모듈의 json() 메소드를 사용한다.

app.get('/', (req, res) => {
  res.send('Hello Wolrd https test completed');
});

app.post('/chat', (req, res) => {
  try {
    // console.log(req.body);
    // Extract the question from the request body (assuming it's sent as JSON)
    const sendedQuestion = req.body.question;
    // console.log(sendedQuestion);

    // EC2 서버에서 현재 실행 중인 Node.js 파일의 절대 경로를 기준으로 설정합니다.
    const scriptPath = path.join(__dirname, 'bizchat.py');
    const pythonPath = path.join(__dirname, 'venv', 'bin', 'python3');

    // Spawn the Python process with the correct argument
    const result = spawn(pythonPath, [scriptPath, sendedQuestion]);

    // result.stdout.on('data', (data) => {
    //   console.log(data.toString());
    //   // return res.status(200).json(data.toString());
    // });

    let responseData = '';

    // Listen for data from the Python script
    result.stdout.on('data', (data) => {
      // console.log(data.toString());
      // res.status(200).json({ answer: data.toString() });
      responseData += data.toString();
    });

    // Listen for errors from the Python script
    result.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
      res.status(500).json({ error: data.toString() });
    });

    // Handle the close event of the child process
    result.on('close', (code) => {
      if (code === 0) {
        res.status(200).json({ answer: responseData });
      } else {
        res
          .status(500)
          .json({ error: `Child process exited with code ${code}` });
      }
    });
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => console.log(`Server is running on ${PORT}`));

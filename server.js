import multer from "multer"
import dotenv from "dotenv"
import fetch from "node-fetch"
import fs from "fs"

dotenv.config()
const app = express()
const upload = multer({ dest: "uploads/" })

const USERS = {
  bara: { pass: "bara1", premium: true },
  free: { pass: "123", premium: false }
}

const usage = {} // limit user free

app.use(express.json())

// ================= ROUTES =================
app.get("/", (req,res)=> res.sendFile(process.cwd()+"/views/login.html"))
app.get("/app", (req,res)=> res.sendFile(process.cwd()+"/views/app.html"))

// ================= LOGIN =================
app.post("/login",(req,res)=>{
  const {user,pass} = req.body
  if(USERS[user] && USERS[user].pass===pass){
    res.json({ok:true,user})
  } else res.json({ok:false})
})

// ================= UPSCALE =================
app.post("/upscale", upload.single("image"), async (req,res)=>{
  const user = req.headers["x-user"]

  if(!USERS[user]) return res.json({error:"login dulu 😐"})

  // limit free user
  if(!USERS[user].premium){
    usage[user] = (usage[user]||0)+1
    if(usage[user] > 3){
      return res.json({error:"limit habis 😹 upgrade premium"})
    }
  }

  try{
    const img = fs.readFileSync(req.file.path,{encoding:"base64"})

    const r = await fetch("https://openrouter.ai/api/v1/images/edits",{
      method:"POST",
      headers:{
        "Authorization": \`Bearer \${process.env.OPENROUTER_API_KEY}\`,
        "Content-Type":"application/json"
      },
      body: JSON.stringify({
        model:"openai/gpt-image-1",
        prompt:"ultra HD, remove blur, sharp, 4k",
        image:\`data:image/png;base64,\${img}\`
      })
    })

    const d = await r.json()
    const result = d.data?.[0]?.url

    fs.unlinkSync(req.file.path)

    res.json({image: result})

  }catch(e){
    res.json({error:true})
  }
})

app.listen(process.env.PORT||3000)

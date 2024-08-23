import { useState ,useEffect} from 'react'
import './App.css'
import data from '../src/assets/jsonfile.json'

function App() {
  const [dat, setdata] = useState(data)

  return (
    <>
      <div className='title'>
        Nobero data Admin Panel
      </div>
      <div className="alldata">

        {dat.map((item)=>{
          return<>
          <div>
            {item.title}
          </div>
          </>
        })
        }
    </div>


    </>
  )
}

export default App

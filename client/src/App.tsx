import './App.css'
import Navbar from './components/Navbar'
import Timer from './components/ClockTimer'
function App() {
  return (
    <>
      <Navbar />
      <div className="App">
        <h1>Welcome to the App!</h1>
      </div>
      <div>
        <Timer/>
      </div>
    </>
  )
}

export default App

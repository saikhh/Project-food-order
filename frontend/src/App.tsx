
import {BrowserRouter as Router, Routes, Route, Link} from 'react-router-dom' 
// @ts-expect-error AuthContext is a JavaScript module without TypeScript declarations.
import {AuthProvider} from './context/AuthContext.jsx'
// @ts-expect-error Register is a JavaScript module without TypeScript declarations.
import Register from './components/Register.jsx';
// @ts-expect-error Login is a JavaScript module without TypeScript declarations.
import Login from './components/Login.jsx';
// @ts-expect-error UserProfile is a JavaScript module without TypeScript declarations.
import UserProfile from './components/UserProfile.jsx';

import './App.css'

function App() {

  return( 
    <Router> 

      <AuthProvider> 
                <div style={{"padding": "20px"}}>
                    <nav>
                        <ul>
                            <li><Link to="/register">Register</Link></li>
                            <li><Link to="/login">Login</Link></li>
                            <li><Link to="/profile">Profile</Link></li>
                        </ul>
                    </nav>
                    <Routes>
                        <Route path="/register" element={<Register/>}/>
                        <Route path="/login" element={<Login/>}/>
                        <Route path="/profile" element={<UserProfile/>}/>
                    </Routes>
                </div>

      </AuthProvider>
    </Router>
  )
}

export default App

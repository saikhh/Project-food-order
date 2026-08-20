import React ,{ useContext} from 'react'; 
import { AuthContext } from '../context/AuthContext'; 

const UserProfile = () => { 

    const { user, logout } = useContext(AuthContext); 

    if(!user) {
        return <p>Please log in to view your profile.</p>; 
    }

    return (
        <div>
            <h2>User Profile</h2>
            <p><strong>Username:</strong> {user.username}</p>
            <p><strong>Email:</strong> {user.email}</p>
            <button onClick={logout}>Logout</button>
        </div>
    );
}

export default UserProfile; 
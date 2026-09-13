import React from 'react'
import { useState, useEffect } from 'react'
import api from '../api'
import { Link } from 'react-router-dom'

const Dashboard = () => {

    const [devices, setDevices] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    useEffect(()=>{
        const fetchDevices = async () => {
            try{
                const response = await api.get('/devices/');
                setDevices(response.data)
            } catch (err) {
                setError('Failed to load devices')
            } finally {
                setLoading(false)
            }
        }

        fetchDevices();

        const interval = setInterval(fetchDevices, 5000)

        return () => clearInterval(interval);
    }, []);

    if (loading) return <p>Loading....</p>
    if (error) return <p>{error}</p>

  return (
    <div>
        <h2>Your Devices</h2>
        {devices.length === 0 ? (
            <p>No devices Yet.</p>
        ) : (
            <ul>
                {devices.map((device) => (
                    <li key={device.id}>
                        <Link to={`/devices/${device.id}`}>
                            <strong>{device.name}</strong> 
                        </Link>
                        {' '}({device.os_type}) - {device.is_online ? '🟢 Online' : '🔴 Offline'}
                        <br />
                        Last seen : {device.last_seen || 'Never'}
                    </li>
                ))}
            </ul>
        )}
    </div>
  )
}

export default Dashboard
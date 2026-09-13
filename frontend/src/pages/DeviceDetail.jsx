import React, { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import api from '../api'

const DeviceDetail = () => {
    const { id } = useParams()
    const [telementry, setTelementry] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const fetchTelementry = async () => {
            try {
                const response = await api.get(`/devices/${id}/telementry/`)
                setTelementry(response.data)
            } catch (err) {
                console.error(err)
            } finally {
                setLoading(false)
            }
        }

        fetchTelementry()
        const interval = setInterval(fetchTelementry, 5000)
        return () => clearInterval(interval)
    }, [id])

    if (loading) return <p>Loading...</p>

    const latest = telementry[0]

    return (
        <div>
            <Link to="/dashboard">Back to dashboard</Link>
            <h2>Device #{id}</h2>
            {latest ? (
                <div>
                    <p>CPU: {latest.cpu_percent}%</p>
                    <p>Memory: {latest.memory_percent}%</p>
                    <p>Disk: {latest.disk_percent}%</p>
                    <p>Last reading: {latest.timestamp}</p>
                </div>
            ) : (
                <p>No telemetry yet.</p>
            )}
        </div>
    )
}

export default DeviceDetail
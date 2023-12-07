import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [health, setHealth] = useState({});
    const [error, setError] = useState(null);

    const getHealth = () => {
        fetch(`http://20.200.126.250:8120/health`)
            .then(res => {
                if (!res.ok) {
                    throw new Error(`HTTP error status: ${res.status}`);
                }
                return res.json();
            })
            .then(
                (result) => {
                    console.log("Received Health", result);
                    setHealth(result);
                    setIsLoaded(true);
                },
                (error) => {
                    setError(error);
                    setIsLoaded(true);
                }
            );
    };
    useEffect(() => {
		const interval = setInterval(() => getHealth(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Health Status</h1>
                <table className={"HealthTable"}>
					<tbody>
						<tr>
							<th>Receiver Status</th>
							<th>Storage Status</th>
							<th>Processor Status</th>
							<th>Audit Status</th>
						</tr>
						<tr>
							<td># Receiver: {health['receiver']}</td>
							<td># Storage: {health['storage']}</td>
							<td># Processor: {health['processor']}</td>
							<td># Audit: {health['audit']}</td>
						</tr>
						<tr>
							<td colspan="2">Count of positive statuses: {stats['num_positive_status']}</td>
						</tr>
					</tbody>
                </table>
                <h3>Last Updated: {health['last_update']}</h3>

            </div>
        )
    }
}

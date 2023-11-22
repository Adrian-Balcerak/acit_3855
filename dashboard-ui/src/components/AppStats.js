import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null);

    const getStats = () => {
        fetch(`http://20.200.126.250:8100/stats`)
            .then(res => {
                if (!res.ok) {
                    throw new Error(`HTTP error status: ${res.status}`);
                }
                return res.json();
            })
            .then(
                (result) => {
                    console.log("Received Stats", result);
                    setStats(result);
                    setIsLoaded(true);
                },
                (error) => {
                    setError(error);
                    setIsLoaded(true);
                }
            );
    };
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>Patrol Reports</th>
							<th>Infrared Reports</th>
						</tr>
						<tr>
							<td># Total Patrol Reports: {stats['num_patrol_reports']}</td>
							<td># Total Infrared Reports: {stats['num_infrared_reports']}</td>
						</tr>
						<tr>
							<td colspan="2">Count of positive statuses: {stats['num_positive_status']}</td>
						</tr>
					</tbody>
                </table>
                <h3>Last Updated: {stats['timestamp']}</h3>

            </div>
        )
    }
}

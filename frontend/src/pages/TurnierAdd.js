import { Box, Typography } from '@mui/material'
import { useEffect, useState } from 'react';


const TurnierAdd = () => {

  const [data, setData] = useState([])

  useEffect(() => {
    fetch('https://jsonplaceholder.typicode.com/users')
      .then((res) => res.json())
      .then((data) => setData(data))
  }, [])

  const renderTable = (array) => {

    return (
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>
          {array.map((e) => (
            <tr key={e.id}>
              <td>{e.username}</td>
              <td>{e.email}</td>
            </tr>
          ))}
        </tbody>
      </table>
    )

  }

  return (
    <div>
      {data && renderTable(data)}
    </div>
  );
}

export default TurnierAdd;
type User = {
  id: number;
  username: string;
  password_hash: string;
};

async function getUsers(): Promise<User[]> {
  const response = await fetch("http://localhost:3000/mysql/users");

  if (!response.ok) {
    throw new Error("Failed to fetch users");
  }

  return response.json();
}

export default async function Home() {
  const users = await getUsers();

  return (
    <main>
      <h1>Users</h1>
      <table style={{ borderCollapse: "collapse", width: "100%", border: "1px solid black" }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.username}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
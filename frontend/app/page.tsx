import { logout } from "@/app/actions/login";
import { redirect } from "next/navigation";
import { getSession } from "./lib/session";
import { HStack, Link, Table, Button } from "@chakra-ui/react/";

type User = {
  id: number;
  username: string;
  email: string;
  password: string;
};

async function getUsers(): Promise<User[]> {
  const response = await fetch("http://localhost:3000/mysql/users");

  if (!response.ok) {
    throw new Error("Failed to fetch users");
  }

  return response.json();
}

export default async function Home() {
  const session = await getSession();

  if (!session.isLoggedIn) {
    redirect('/login');
  }

  const users = await getUsers();

  return (
    <main>
      <h1>Users</h1>
      <Table.Root style={{ borderCollapse: "collapse", width: "100%", border: "1px solid black" }}>
        <Table.Caption />
        <Table.Header>
          <Table.Row>
            <Table.ColumnHeader>ID</Table.ColumnHeader>
            <Table.ColumnHeader>Username</Table.ColumnHeader>
            <Table.ColumnHeader>Email</Table.ColumnHeader>
            <Table.ColumnHeader>Password Hash</Table.ColumnHeader>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {users.map((user) => (
            <Table.Row key={user.id}>
              <Table.Cell>{user.id}</Table.Cell>
              <Table.Cell>{user.username}</Table.Cell>
              <Table.Cell>{user.email}</Table.Cell>
              <Table.Cell>{user.password}</Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
        <Table.Footer>
          <Table.Row>
            <Table.Cell />
          </Table.Row>
        </Table.Footer>
      </Table.Root>
      <HStack>
        <Link href="/game"><Button>Go to Game</Button></Link>
        <Link onClick={logout}><Button>Logout</Button></Link>
      </HStack>
    </main>
  );
}
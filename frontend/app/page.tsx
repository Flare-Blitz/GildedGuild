import { logout } from "@/app/actions/login";
import { redirect } from "next/navigation";
import { getSession } from "./lib/session";
import { HStack, Link, Table, Button, Card } from "@chakra-ui/react/";

type User = {
  user_id: number;
  username: string;
  email: string;
  password: string;
};

async function getUsers(): Promise<User[]> {
  const response = await fetch("http://localhost:3000/mysql/users");

  console.log(response);
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

  return (
    <main>
      <Card.Root>
        <Card.Body>
          <Card.Title>Welcome, {session.username}!</Card.Title>
        </Card.Body>
      </Card.Root>
      
      <HStack>
        <Link href="/game"><Button>Go to Game</Button></Link>
        <Link onClick={logout}><Button>Logout</Button></Link>
      </HStack>
    </main>
  );
}
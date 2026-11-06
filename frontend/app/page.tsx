import { logout } from "@/app/actions/login";
import { redirect } from "next/navigation";
import { getSession } from "./lib/session";
import { HStack, Link, Button, Card } from "@chakra-ui/react/";


export default async function Home() {
  const session = await getSession();

  if (!session.isLoggedIn) {
    redirect('/login');
  }

  return (
    <main>
      <Card.Root>
        <Card.Body>
          <Card.Title id="title-card">Welcome, {session.username}!</Card.Title>
        </Card.Body>
      </Card.Root>
      
      <HStack>
        <Link id="go-to-game" href="/game"><Button>Go to Game</Button></Link>
        <Link onClick={logout}><Button>Logout</Button></Link>
      </HStack>
    </main>
  );
}
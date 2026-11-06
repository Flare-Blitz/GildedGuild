import SignupForm from '@/app/ui/signup-form'
import { Heading } from '@chakra-ui/react/';

export default async function Home() {

  return (
    <div>
        <main style={{ padding: "20px", 
          border: "1px solid #ccc", 
          borderRadius: "5px", 
          margin: "20px" }}>
          <Heading size="xl">Sign Up</Heading>
          <SignupForm />
        </main>
    </div>
  );
}
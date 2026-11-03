import { Field, Input, Box, Button, Link, Heading } from "@chakra-ui/react";
import { login } from "../actions/login";

export default async function Login() {
  return (
    <main className="p-10 space-y-5">
      <Heading size="xl">Gilded Guild Login</Heading>

      <div style={{ padding: "20px", border: "1px solid #ccc", borderRadius: "5px", margin: "20px" }}>

        <form action={login}>
          <Box >
            <Field.Root required>
              <Field.Label>
                Username <Field.RequiredIndicator />
              </Field.Label>
              <Input id="username" name="username" placeholder="Enter your username" />
            </Field.Root>
            <Field.Root required>
              <Field.Label>
                Password <Field.RequiredIndicator />
              </Field.Label>
              <Input id="password" name="password" type="password" placeholder="Password" />
            </Field.Root>
          </Box>
          <Button type="submit">Login</Button>
        </form>
        <div>
          <p>Don&apos;t have an account? <Link href="/register" color="teal.500">Register</Link></p>
        </div>
      </div>
    </main>
  );
}
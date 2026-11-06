'use client'

import { signup } from '@/app/actions/auth'
import { Button, Field, Input } from '@chakra-ui/react/'
import { useActionState } from 'react'

export default function SignupForm() {
  const [state, action, pending] = useActionState(signup, undefined)

  return (
    <form action={action}>
      <Field.Root invalid={!!state?.errors?.name}>
        <Field.Label>Username</Field.Label>
        <Input id="username" name="username" placeholder="Enter your username" />
        {state?.errors?.name && <Field.ErrorText>{state.errors.name}</Field.ErrorText>}
      </Field.Root>
      {state?.message && <p>{state.message}</p>}
      

      <Field.Root invalid={!!state?.errors?.email}>
        <Field.Label>Email</Field.Label>
        <Input id="email" name="email" placeholder="Enter your email" />
        {state?.errors?.email && <Field.ErrorText>{state.errors.email}</Field.ErrorText>}
      </Field.Root>

      <Field.Root invalid={!!state?.errors?.password}>
        <Field.Label>Password</Field.Label>
        <Input id="password" name="password" type="password" placeholder="Enter your password" />
        {state?.errors?.password && (
          <Field.ErrorText>
            <p>Password must:</p>
            <ul>
              {state.errors.password.map((error) => (
                <li key={error}>- {error}</li>
              ))}
            </ul>
          </Field.ErrorText>
        )}
      </Field.Root>
      <Button type="submit" disabled={pending}>Sign Up</Button>
    </form>
  )
}
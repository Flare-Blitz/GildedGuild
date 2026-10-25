import SignupForm from '@/app/ui/signup-form'

export default async function Home() {

  return (
    <div>
        <main style={{ padding: "20px", 
          border: "1px solid #ccc", 
          borderRadius: "5px", 
          margin: "20px" }}>
          <h1>Sign Up</h1>
          <SignupForm />
        </main>
    </div>
  );
}
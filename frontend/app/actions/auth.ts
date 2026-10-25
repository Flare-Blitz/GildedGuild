"use server";

import bcrypt from "bcryptjs";
import mysql from "mysql2/promise";
import { SignupFormSchema, FormState } from "@/app/lib/definitions";
import { getSession } from "@/app/lib/session";
import type { ResultSetHeader } from "mysql2";
import { redirect } from "next/navigation";

const pool = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: Number(process.env.DB_PORT ?? 3306),
});

export async function signup(
  state: FormState,
  formData: FormData
): Promise<FormState> {
  const validatedFields = SignupFormSchema.safeParse({
    name: formData.get("name"),
    email: formData.get("email"),
    password: formData.get("password"),
  });

  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    };
  }

  const { name, email, password } = validatedFields.data;
  const hashedPassword = await bcrypt.hash(password, 10);

  try 
  {
    const [result] = await pool.execute<ResultSetHeader>(
    `INSERT INTO users (username, email, password)
    VALUES (?, ?, ?)`,
    [name, email, hashedPassword]
    );

    const session = await getSession();

    session.id = result.insertId;
    session.username = name;
    session.email = email;
    session.isLoggedIn = true;

    await session.save();

    redirect('/');
  } 
  catch (error) 
  {
    console.error("Signup failed:", error);

    return {
      message: "An error occurred while creating your account.",
    };
  }
}
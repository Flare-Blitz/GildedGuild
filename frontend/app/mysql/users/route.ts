import mysql from "mysql2/promise";
import { NextResponse } from "next/server";

const pool = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: Number(process.env.DB_PORT ?? 3306),
});

export async function GET() {
  const [rows] = await pool.query(
    "SELECT id, username FROM users ORDER BY id"
  );

  return NextResponse.json(rows);
}
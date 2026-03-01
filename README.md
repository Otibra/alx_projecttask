Task Management API

A RESTful API built with Django REST Framework to practice backend development concepts such as authentication, role-based access control (RBAC), and filtering and sorting.

This project focuses on implementing a clean, secure CRUD API for tasks and projects with user roles.

About The Project

The Task Management API allows users to:

Register and log in securely using JWT

Create, update, and manage tasks

Organize tasks into projects

Assign tasks to users

Filter and sort task lists

Restrict access based on user roles (Admin / Manager / User)

The project was built to strengthen understanding of backend architecture, secure API design, and role-based authorization.

. Authentication & Authorization JWT Authentication

Secure login system using JSON Web Tokens

Stateless authentication

Token refresh support

Role-Based Access Control (RBAC)

The system supports three roles:

Admin – Full access

Manager – Manage projects and assigned tasks

User – Manage their own tasks

Access is enforced consistently across the API to maintain security and simplicity.

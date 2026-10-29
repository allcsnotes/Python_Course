CREATE TABLE students (
    id            serial PRIMARY KEY,
    email         text NOT NULL UNIQUE,
    password_hash text NOT NULL,
    role          text NOT NULL DEFAULT 'student'
);
CREATE TABLE courses (
    id    serial PRIMARY KEY,
    title text NOT NULL UNIQUE,
    price int  NOT NULL CHECK (price > 0)
);
CREATE TABLE lessons (
    id        serial PRIMARY KEY,
    course_id int  NOT NULL REFERENCES courses(id),
    position  int  NOT NULL,
    title     text NOT NULL,
    UNIQUE (course_id, position)
);
CREATE TABLE enrollments (
    id          serial PRIMARY KEY,
    student_id  int NOT NULL REFERENCES students(id),
    course_id   int NOT NULL REFERENCES courses(id),
    enrolled_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (student_id, course_id)
);
CREATE TABLE lesson_progress (
    enrollment_id int NOT NULL REFERENCES enrollments(id),
    lesson_id     int NOT NULL REFERENCES lessons(id),
    completed_at  timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (enrollment_id, lesson_id)
);
CREATE TABLE certificates (
    id            serial PRIMARY KEY,
    enrollment_id int NOT NULL UNIQUE REFERENCES enrollments(id),
    status        text NOT NULL DEFAULT 'pending'
                  CHECK (status IN ('pending', 'sent')),
    attempts      int  NOT NULL DEFAULT 0,
    created_at    timestamptz NOT NULL DEFAULT now(),
    sent_at       timestamptz
);
CREATE TABLE idempotency_keys (
    student_id   int  NOT NULL REFERENCES students(id),
    key          text NOT NULL,
    request_hash text NOT NULL,
    status_code  int  NOT NULL,
    body         jsonb NOT NULL,
    created_at   timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (student_id, key)
);

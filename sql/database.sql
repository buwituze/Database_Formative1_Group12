-- Table: Person
CREATE TABLE Person (
    PersonID INT PRIMARY KEY IDENTITY(1,1),
    Age INT NOT NULL,
    Gender VARCHAR(10) NOT NULL
);

-- Table: Education
CREATE TABLE Education (
    EducationID INT PRIMARY KEY IDENTITY(1,1),
    EducationLevel VARCHAR(50) NOT NULL
);

-- Table: Job
CREATE TABLE Job (
    JobID INT PRIMARY KEY IDENTITY(1,1),
    PersonID INT NOT NULL,
    EducationID INT NOT NULL,
    JobTitle VARCHAR(100) NOT NULL,
    YearsOfExperience INT NOT NULL,
    Salary DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID),
    FOREIGN KEY (EducationID) REFERENCES Education(EducationID)
);

-- Table: SalaryLog
CREATE TABLE SalaryLog (
    LogID INT PRIMARY KEY IDENTITY(1,1),
    JobID INT,
    OldSalary DECIMAL(12,2),
    NewSalary DECIMAL(12,2),
    ChangeDate DATETIME DEFAULT GETDATE()
);

-- Stored Procedure: InsertJob
CREATE PROCEDURE InsertJob
    @PersonID INT,
    @EducationID INT,
    @JobTitle VARCHAR(100),
    @YearsOfExperience INT,
    @Salary DECIMAL(12,2)
AS
BEGIN
    IF @Salary < 0
    BEGIN
        RAISERROR('Salary cannot be negative.', 16, 1);
        RETURN;
    END

    INSERT INTO Job (PersonID, EducationID, JobTitle, YearsOfExperience, Salary)
    VALUES (@PersonID, @EducationID, @JobTitle, @YearsOfExperience, @Salary);
END
GO

-- Trigger: Log Salary Changes
CREATE TRIGGER trg_LogSalaryChange
ON Job
AFTER UPDATE
AS
BEGIN
    IF UPDATE(Salary)
    BEGIN
        INSERT INTO SalaryLog (JobID, OldSalary, NewSalary)
        SELECT i.JobID, d.Salary, i.Salary
        FROM inserted i
        JOIN deleted d ON i.JobID = d.JobID
        WHERE i.Salary <> d.Salary;
    END
END
GO
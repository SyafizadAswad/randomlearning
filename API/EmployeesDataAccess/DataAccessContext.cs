using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using EmployeesDataAccess.Models;

namespace EmployeesDataAccess
{
    public class DataAccessContext: DbContext
    {
        public DataAccessContext(DbContextOptions<DataAccessContext> options) : base(options) { }

        public DbSet<Employee> Employee { get; set; }

        public DbSet<Department> Department { get; set; }
    }
}

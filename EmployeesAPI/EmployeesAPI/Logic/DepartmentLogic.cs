using EmployeesDataAccess.Models;
using EmployeesDataAccess.Interfaces;
using EmployeesAPI.Model;
using EmployeesAPI.Interfaces;
using EmployeesAPI.Exceptions;

namespace EmployeesAPI.Logic
{
    public class DepartmentLogic : IDepartmentLogic
    {
        private readonly IDepartmentRepository _departmentRepository;

        public DepartmentLogic(IDepartmentRepository departmentRepository)
        {
            _departmentRepository = departmentRepository;
        }

        public async Task<IEnumerable<DepartmentResponse>> GetAllDepartment()
        {
            var departments = await _departmentRepository.GetAllDepartmentAsync();

            return departments.Select(e => new DepartmentResponse
            {
                DepartmentId = e.DepartmentId,
                DepartmentName = e.DepartmentName
            });
        }
    }
}

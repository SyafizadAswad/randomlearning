using EmployeesAPI.Model;

namespace EmployeesAPI.Interfaces
{
    public interface IDepartmentLogic
    {
        Task<IEnumerable<DepartmentResponse>> GetAllDepartment();
    }
}

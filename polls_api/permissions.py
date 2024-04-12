from rest_framework import permissions

#로그인된 사용자, 즉 자기가 작성한 글만 수정할 수 있도록(보기는 아무나 가능)
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request,view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.owner ==request.user
    
#voter만이 접근할 수 있는 권한    
class IsVoter(permissions.BasePermission):
    def has_object_permission(self, request,view, obj): 
        return obj.voter == request.user    
def panel_permissions(request):
    """
    صلاحيات المستخدم في القالب
    """
    if not request.user.is_authenticated:
        return {
            'has_applications_access': False,
            'has_certificates_access': False,
            'has_contact_access': False,
            'has_access_access': False,
            'has_universities_access': False,
            'has_announcements_access': False,
            'has_guide_access': False,
            'has_data_entry_access': False,
            'is_super_admin': False,
        }

    try:
        profile = request.user.profile
        return {
            'has_applications_access': profile.has_section_access('applications'),
            'has_certificates_access': profile.has_section_access('certificates'),
            'has_contact_access': profile.has_section_access('contact'),
            'has_access_access': profile.has_section_access('access'),
            'has_universities_access': profile.has_section_access('universities'),
            'has_announcements_access': profile.has_section_access('announcements'),
            'has_guide_access': profile.has_section_access('guide'),
            'has_data_entry_access': profile.has_section_access('data_entry'),
            'is_super_admin': profile.is_super_admin,
        }
    except Exception:
        return {
            'has_applications_access': False,
            'has_certificates_access': False,
            'has_contact_access': False,
            'has_access_access': False,
            'has_universities_access': False,
            'has_announcements_access': False,
            'has_guide_access': False,
            'has_data_entry_access': False,
            'is_super_admin': request.user.is_superuser,
        }
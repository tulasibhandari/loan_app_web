from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import formset_factory, modelformset_factory
from .forms import (
    CollateralBasicForm,
    CollateralPropertyForm,
    CollateralFamilyDetailForm,
    CollateralIncomeExpenseForm,
    CollateralAffiliationForm,
)
from .models import (
    CollateralBasic,
    CollateralProperty,
    CollateralFamilyDetail,
    CollateralIncomeExpense,
    CollateralAffiliation,
)
from members.models import Member


@login_required
def basic_form(request, member_number):
    """Collateral Basic information form"""
    member = get_object_or_404(Member, member_number=member_number)
    instance = CollateralBasic.objects.filter(member=member).first()

    if request.method == 'POST':
        form = CollateralBasicForm(request.POST, instance=instance)
        if form.is_valid():
            collateral = form.save(commit=False)
            collateral.member = member
            collateral.save()
            messages.success(request, 'आधारभूत धितो जानकारी सेभ भयो।')
            return redirect('collateral:property_form', member_number=member_number)
        else:
            messages.error(request, 'कृपया फाराम सही तरिकाले भर्नुहोस्।')
    else:
        form = CollateralBasicForm(instance=instance)

    return render(request, 'collateral/basic_form.html', {
        'form': form,
        'member': member,
        'step': 1,
        'total_steps': 5,
        'step_name': 'आधारभूत जानकारी',
    })


@login_required
def property_form(request, member_number):
    """Collateral Property details (Dhito Bibaran)"""
    member = get_object_or_404(Member, member_number=member_number)
    properties = CollateralProperty.objects.filter(member=member)

    PropertyFormSet = modelformset_factory(
        CollateralProperty,
        form=CollateralPropertyForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        formset = PropertyFormSet(request.POST, queryset=properties)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.member = member
                instance.save()
            for obj in formset.deleted_objects:
                obj.delete()
            messages.success(request, 'जग्गा धितो जानकारी सेभ भयो।')
            return redirect('collateral:family_form', member_number=member_number)
        else:
            messages.error(request, 'कृपया फाराम सही तरिकाले भर्नुहोस्।')
    else:
        formset = PropertyFormSet(queryset=properties)

    return render(request, 'collateral/property_form.html', {
        'formset': formset,
        'member': member,
        'step': 2,
        'total_steps': 5,
        'step_name': 'जग्गा धितो विवरण',
    })


@login_required
def family_form(request, member_number):
    """Family details for collateral"""
    member = get_object_or_404(Member, member_number=member_number)
    family_members = CollateralFamilyDetail.objects.filter(member=member)

    FamilyFormSet = modelformset_factory(
        CollateralFamilyDetail,
        form=CollateralFamilyDetailForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        formset = FamilyFormSet(request.POST, queryset=family_members)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.member = member
                instance.save()
            for obj in formset.deleted_objects:
                obj.delete()
            messages.success(request, 'परिवार विवरण सेभ भयो।')
            return redirect('collateral:income_expense_form', member_number=member_number)
        else:
            messages.error(request, 'कृपया फाराम सही तरिकाले भर्नुहोस्।')
    else:
        formset = FamilyFormSet(queryset=family_members)

    return render(request, 'collateral/family_form.html', {
        'formset': formset,
        'member': member,
        'step': 3,
        'total_steps': 5,
        'step_name': 'परिवार विवरण',
    })


@login_required
def income_expense_form(request, member_number):
    """Income and Expense tracking"""
    member = get_object_or_404(Member, member_number=member_number)
    income_items = CollateralIncomeExpense.objects.filter(member=member, type='income')
    expense_items = CollateralIncomeExpense.objects.filter(member=member, type='expense')

    IncomeFormSet = modelformset_factory(
        CollateralIncomeExpense,
        form=CollateralIncomeExpenseForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        income_formset = IncomeFormSet(
            request.POST,
            queryset=income_items,
            prefix='income'
        )
        expense_formset = IncomeFormSet(
            request.POST,
            queryset=expense_items,
            prefix='expense'
        )

        if income_formset.is_valid() and expense_formset.is_valid():
            for formset, ie_type in [(income_formset, 'income'), (expense_formset, 'expense')]:
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.member = member
                    instance.type = ie_type
                    instance.save()
                for obj in formset.deleted_objects:
                    obj.delete()
            messages.success(request, 'आय/व्यय विवरण सेभ भयो।')
            return redirect('collateral:affiliation_form', member_number=member_number)
        else:
            messages.error(request, 'कृपया फाराम सही तरिकाले भर्नुहोस्।')
    else:
        income_formset = IncomeFormSet(queryset=income_items, prefix='income')
        expense_formset = IncomeFormSet(queryset=expense_items, prefix='expense')

    return render(request, 'collateral/income_expense_form.html', {
        'income_formset': income_formset,
        'expense_formset': expense_formset,
        'member': member,
        'step': 4,
        'total_steps': 5,
        'step_name': 'आय/व्यय विवरण',
    })


@login_required
def affiliation_form(request, member_number):
    """Organizational Affiliations"""
    member = get_object_or_404(Member, member_number=member_number)
    affiliations = CollateralAffiliation.objects.filter(member=member)

    AffiliationFormSet = modelformset_factory(
        CollateralAffiliation,
        form=CollateralAffiliationForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        formset = AffiliationFormSet(request.POST, queryset=affiliations)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.member = member
                instance.save()
            for obj in formset.deleted_objects:
                obj.delete()
            messages.success(request, 'संस्था सम्बन्ध विवरण सेभ भयो।')
            # Redirect to loan detail or member detail after all collateral done
            return redirect('members:member_detail', member_number=member_number)
        else:
            messages.error(request, 'कृपया फाराम सही तरिकाले भर्नुहोस्।')
    else:
        formset = AffiliationFormSet(queryset=affiliations)

    return render(request, 'collateral/affiliation_form.html', {
        'formset': formset,
        'member': member,
        'step': 5,
        'total_steps': 5,
        'step_name': 'संस्था सम्बन्ध',
    })


@login_required
def collateral_overview(request, member_number):
    """Overview of all collateral info for a member"""
    member = get_object_or_404(Member, member_number=member_number)
    basic = CollateralBasic.objects.filter(member=member).first()
    properties = CollateralProperty.objects.filter(member=member)
    family = CollateralFamilyDetail.objects.filter(member=member)
    income = CollateralIncomeExpense.objects.filter(member=member, type='income')
    expense = CollateralIncomeExpense.objects.filter(member=member, type='expense')
    affiliations = CollateralAffiliation.objects.filter(member=member)

    total_income = sum(float(i.amount or 0) for i in income)
    total_expense = sum(float(e.amount or 0) for e in expense)

    return render(request, 'collateral/overview.html', {
        'member': member,
        'basic': basic,
        'properties': properties,
        'family': family,
        'income': income,
        'expense': expense,
        'affiliations': affiliations,
        'total_income': total_income,
        'total_expense': total_expense,
        'net_income': total_income - total_expense,
    })
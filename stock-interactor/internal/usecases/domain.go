package usecases

type domainStruct struct {
	transport transport
}

func New(transport transport) domainStruct {
	return domainStruct{
		transport: transport,
	}
}
